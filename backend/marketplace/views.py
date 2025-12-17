import stripe
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Programmer, Project
from .serializers import ProgrammerSerializer, ProjectSerializer

if hasattr(settings, 'STRIPE_SECRET_KEY'):
    stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['GET'])
@permission_classes([AllowAny])
def programmer_list(request):
    programmers = Programmer.objects.all()

    category = request.GET.get('category')
    search = request.GET.get('search')
    if category:
        programmers = programmers.filter(category__icontains=category)
    if search:
        programmers = programmers.filter(name__icontains=search)
        
    serializer = ProgrammerSerializer(programmers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def programmer_detail(request, id):
    programmer = get_object_or_404(Programmer, id=id)
    serializer = ProgrammerSerializer(programmer)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_programmer(request, id):
    programmer = get_object_or_404(Programmer, id=id)
    new_rating = request.data.get('rating')
    if new_rating:
        total_score = programmer.rating * programmer.review_count
        programmer.review_count += 1
        programmer.rating = (total_score + float(new_rating)) / programmer.review_count
        programmer.save()
        return Response({'message': 'Rating added', 'new_rating': programmer.rating})
    return Response({'error': 'Rating not provided'}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def increment_profile_views(request, id):
    try:
        programmer = Programmer.objects.get(id=id)
        programmer.profile_views += 1
        programmer.save()
        return Response({'profileViews': programmer.profile_views})
    except Programmer.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

@api_view(['POST'])
@permission_classes([AllowAny])
def increment_contact_clicks(request, id):
    return Response({'message': 'Click recorded'})

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    user = request.user
    
    if request.method == 'PATCH':
        data = request.data
        user.username = data.get('username', user.username)
        user.save()
        
        try:
            programmer = Programmer.objects.get(user=user)
            programmer.name = user.username # Sync name
            if 'category' in data: programmer.category = data['category']
            if 'bio' in data: programmer.bio = data['bio']
            if 'skills' in data: programmer.skills = data['skills']
            if 'portfolio' in data: programmer.portfolio_url = data['portfolio']
            if 'imageUrl' in data: programmer.image_url = data['imageUrl']
            programmer.save()
            
            serializer = ProgrammerSerializer(programmer)
            resp_data = dict(serializer.data)
            resp_data['user_type'] = 'freelancer'
            return Response(resp_data)
        except Programmer.DoesNotExist:
            return Response({'message': 'Profile updated', 'username': user.username})



    try:
        programmer = Programmer.objects.get(user=user)
        serializer = ProgrammerSerializer(programmer)
        
    
        data = dict(serializer.data)
        data['user_type'] = 'freelancer' 
        return Response(data)
        
    except Programmer.DoesNotExist:
        client_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'user_type': 'client', 
            'category': None,
            'bio': '',
            'skills': [],          
            'portfolio': '',
            'imageUrl': '',
            'rating': 0,
            'totalRatings': 0,
            'profileViews': 0,
            'contactClicks': 0
        }
        return Response(client_data)

from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def contact_us(request):
    return Response({'message': 'Message sent successfully'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_projects(request):
    user = request.user
    
    hired = Project.objects.filter(client=user)
    
    try:
        programmer_profile = Programmer.objects.get(user=user)
        work = Project.objects.filter(freelancer=programmer_profile)
    except Programmer.DoesNotExist:
        work = Project.objects.none()

    return Response({
        "hired_projects": ProjectSerializer(hired, many=True).data,
        "work_projects": ProjectSerializer(work, many=True).data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_project(request, freelancer_id):
    try:
        freelancer = Programmer.objects.get(id=freelancer_id)
    except Programmer.DoesNotExist:
        return Response({'error': 'Freelancer not found'}, status=404)

    data = request.data
    project = Project.objects.create(
        client=request.user,
        freelancer=freelancer,
        title=data.get('title', 'New Project'),
        description=data.get('description', 'Project Request'),
        amount=data.get('amount', 50.00) 
    )
    return Response(ProjectSerializer(project).data, status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    try:
        programmer = Programmer.objects.get(user=request.user)
        if project.freelancer != programmer:
             return Response({'error': 'Not authorized'}, status=403)
    except Programmer.DoesNotExist:
        return Response({'error': 'Not a freelancer'}, status=403)

    if project.status == 'pending':
        project.status = 'active'
        project.save()
        return Response({'status': 'Project accepted and active'})
    
    return Response({'error': 'Project already active or processed'}, status=400)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
        
    serializer = ProjectSerializer(project, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_intent(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        amount_cents = int(project.amount * 100)
        
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency='usd',
            metadata={'project_id': project.id}
        )
        
        return Response({'clientSecret': intent['client_secret']})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_payment(request, payment_id):
    return Response({'status': 'payment confirmed'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_project_payment_status(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.is_paid = True
    project.status = 'active' 
    project.save()
    project.save()
    return Response({'status': 'Project is now active'})

# ADMIN PROJECT VIEWS
from rest_framework import generics
from accounts.permissions import IsSuperUser

class AdminProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsSuperUser]

class AdminDeleteProjectView(generics.DestroyAPIView):
    queryset = Project.objects.all()
    permission_classes = [IsSuperUser]
    lookup_field = 'id'