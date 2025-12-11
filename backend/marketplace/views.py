from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny
)
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings

from .models import Programmer, Rating
from .serializers import ProgrammerSerializer

#View list + Search
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
        paginated = paginator.paginate_queryset(programmers, request)
        serializer = ProgrammerSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = ProgrammerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# 2. DETAIL PAGE (GET, EDIT, DELETE)
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
                skills_data = request.data['skills']
                if isinstance(skills_data, list):
                    programmer.skills = ",".join(skills_data)
                else:
                    programmer.skills = str(skills_data)
                programmer.save()

            serializer.save()
            return Response(ProgrammerSerializer(programmer).data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        programmer.delete()
        return Response(status=204)


#Rating Logic (Average)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_programmer(request, id):
    try:
        programmer = Programmer.objects.get(id=id)
    except Programmer.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    stars = request.data.get("rating") or request.data.get("stars")
    if not stars:
        return Response({'error': 'Rating (1–5) required'}, status=400)

    try:
        stars = int(stars)
        if stars < 1 or stars > 5:
            return Response({'error': 'Rating must be between 1 and 5'}, status=400)
    except ValueError:
        return Response({'error': 'Invalid rating'}, status=400)



    current_total_score = programmer.rating * programmer.review_count
    programmer.review_count += 1
    new_average = (current_total_score + new_star_value) / programmer.review_count
    
    programmer.rating = round(new_average, 2)
    programmer.save()

    # 🔥 IMPORTANT: Reload the programmer to recalc values
    programmer.refresh_from_db()

    # Serialize with updated average + count
    serializer = ProgrammerSerializer(programmer)
    return Response(serializer.data)


# Personal Profile (DASHBOARD SAVE FIX)
@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    user = request.user
    try:
        profile = Programmer.objects.get(user=user)
    except Programmer.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=404)

    if request.method == 'GET':
        return Response(ProgrammerSerializer(profile).data)

    if request.method in ['PUT', 'PATCH']:

        data = request.data.copy()

        if 'skills' in data:
            skills_data = data['skills']
            if isinstance(skills_data, list):
                

                profile.skills = ",".join(skills_data)
            else:
                profile.skills = str(skills_data)
            
            profile.save() 
            
            
            if isinstance(data, dict):
                del data['skills']
            else:
                data._mutable = True
                data.pop('skills', None)
                data._mutable = False



        serializer = ProgrammerSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(ProgrammerSerializer(profile).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Counters
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



# 6. INCREASE CONTACT CLICKS
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


# Contact Us
@api_view(['POST'])
@permission_classes([AllowAny])
def contact_us(request):
    name = request.data.get('name')
    email = request.data.get('email')
    message = request.data.get('message')

    if not name or not message:
        return Response({'error': 'Name and Message required'}, status=400)

    subject = f"New message from {name}"
    full_message = f"""
    New message from SoftwJob:

    Name: {name}
    Email: {email}

    Message:
    {message}
    """

    try:
        send_mail(
            subject=subject,
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.COMPANY_EMAIL],
            fail_silently=False,
        )
        return Response({'message': 'Email sent successfully!'})
    except Exception as e:
        print("Email Error:", e)
        return Response({'error': 'Failed to send email'}, status=500)
