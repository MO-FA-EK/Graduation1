from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Q

from .models import Programmer
from .serializers import ProgrammerSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def programmer_list(request):
    if request.method == 'GET':
        programmers = Programmer.objects.all()
        search_query = request.GET.get('search')
        
        if search_query:
            programmers = programmers.filter(
                Q(name__icontains=search_query) |       
                Q(skills__icontains=search_query) |     
                Q(category__icontains=search_query) |   
                Q(bio__icontains=search_query)          
            )

        paginator = LimitOffsetPagination()
        paginated_programmers = paginator.paginate_queryset(programmers, request)
        serializer = ProgrammerSerializer(paginated_programmers, many=True)
        return paginator.get_paginated_response(serializer.data)


    serializer = ProgrammerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def programmer_detail(request, id):
    try:
        programmer = Programmer.objects.get(id=id)
    except Programmer.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        return Response(ProgrammerSerializer(programmer).data)

    if request.method in ['PUT', 'PATCH']:
        serializer = ProgrammerSerializer(programmer, data=request.data, partial=True)
        if serializer.is_valid():

            if 'skills' in request.data:
                programmer.skills = request.data['skills']
                programmer.save()
                
            serializer.save()
            return Response(ProgrammerSerializer(programmer).data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        programmer.delete()
        return Response(status=204)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_programmer(request, id):
    try:
        programmer = Programmer.objects.get(id=id)
    except Programmer.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    new_rating = request.data.get('rating')
    if new_rating is None:
        return Response({'error': 'Rating required'}, status=400)

    try:
        new_star_value = float(new_rating)
    except ValueError:
        return Response({'error': 'Invalid rating'}, status=400)

    current_total_score = programmer.rating * programmer.review_count
    programmer.review_count += 1
    new_average = (current_total_score + new_star_value) / programmer.review_count
    
    programmer.rating = round(new_average, 2)
    programmer.save()

   
    return Response(ProgrammerSerializer(programmer).data)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    user = request.user
    try:
        profile = Programmer.objects.get(user=user)
    except Programmer.DoesNotExist:
        return Response({'error': 'Profile not found for this user'}, status=404)

    if request.method == 'GET':
        return Response(ProgrammerSerializer(profile).data)

    if request.method in ['PUT', 'PATCH']:
        serializer = ProgrammerSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            if 'skills' in request.data:
                profile.skills = request.data['skills']
                profile.save()
            serializer.save()
            return Response(ProgrammerSerializer(profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def increment_profile_views(request, id):
    try:
        p = Programmer.objects.get(id=id)
        p.profile_views += 1
        p.save()
        return Response({'profileViews': p.profile_views})
    except Programmer.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

@api_view(['POST'])
@permission_classes([AllowAny])
def increment_contact_clicks(request, id):
    try:
        p = Programmer.objects.get(id=id)
        p.contact_clicks += 1
        p.save()
        return Response({'contactClicks': p.contact_clicks})
    except Programmer.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)