# marketplace/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

from .models import User                   # programmer table (your model)
from .serializers import UserSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])  # GET open, POST requires JWT
def programmer_list(request):
    if request.method == 'GET':
        users = User.objects.all()

        # Filters
        skill = request.GET.get('skill')
        name = request.GET.get('name')
        if skill:
            users = users.filter(skills__icontains=skill)
        if name:
            users = users.filter(name__icontains=name)

        # Ordering
        ordering_param = request.GET.get('ordering')
        if ordering_param:
            users = users.order_by(ordering_param)

        # Pagination
        paginator = LimitOffsetPagination()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)

    # POST (requires JWT)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticatedOrReadOnly])  # write ops need JWT
def programmer_detail(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({'error': 'Programmer not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # PUT/PATCH
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # only authenticated users can rate
def rate_programmer(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({'error': 'Programmer not found'}, status=status.HTTP_404_NOT_FOUND)

    new_rating = request.data.get('rating')
    if new_rating is None:
        return Response({'error': 'Rating value required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        new_rating = float(new_rating)
        if not (0 <= new_rating <= 5):
            return Response({'error': 'Rating must be between 0 and 5'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'Rating must be a number'}, status=status.HTTP_400_BAD_REQUEST)

    total_reviews = user.review_count + 1
    total_rating = (user.rating * user.review_count + new_rating) / total_reviews

    user.rating = round(total_rating, 2)
    user.review_count = total_reviews
    user.save()

    serializer = UserSerializer(user)
    return Response(serializer.data)


# ---------------------------
# NEW: /api/profile/ endpoint
# ---------------------------
@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])  # must be logged in
def my_profile(request):
    """
    Return or update the logged-in user's programmer profile.
    We link auth user <-> programmer row primarily by email.
    If no matching row exists, create one with sensible defaults.
    """
    auth_user = request.user

    # Prefer email match; fall back to username if email is empty
    lookup = {}
    if getattr(auth_user, 'email', None):
        lookup['email'] = auth_user.email
    else:
        lookup['name'] = auth_user.username

    profile, created = User.objects.get_or_create(
        **lookup,
        defaults={
            'name': auth_user.username,
            'email': getattr(auth_user, 'email', '') or '',
            'skills': '',
            'image': None,
            'rating': 0.0,
            'review_count': 0,
            'category': 'General',
            'experience_level': 'Beginner',
            'bio': None,
        }
    )

    if request.method == 'GET':
        return Response(UserSerializer(profile).data)

    # Allow partial updates for both PUT/PATCH to keep it simple
    serializer = UserSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        # Extra safety: ignore attempts to modify rating counters
        serializer.validated_data.pop('rating', None)
        serializer.validated_data.pop('review_count', None)
        obj = serializer.save()
        return Response(UserSerializer(obj).data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
