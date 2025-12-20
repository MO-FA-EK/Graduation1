import stripe
import requests
from django.db.models import Q
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail
from rest_framework import generics
from .models import Programmer, Project, ContactMessage
from .serializers import ProgrammerSerializer, ProjectSerializer, ContactMessageSerializer

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
        programmers = programmers.filter(
            Q(name__icontains=search) | 
            Q(user__username__icontains=search) |
            Q(bio__icontains=search) |
            Q(skills__icontains=search) |
            Q(category__icontains=search)
        )
        
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
        if 'username' in data:
            user.username = data['username']
            user.save()
        
        try:
            programmer = Programmer.objects.get(user=user)
            programmer.name = user.username 
            if 'category' in data: programmer.category = data['category']
            if 'bio' in data: programmer.bio = data['bio']
            if 'skills' in data: programmer.skills = data['skills']
            if 'portfolio' in data: programmer.portfolio_url = data['portfolio']
            if 'imageUrl' in data: programmer.image_url = data['imageUrl']
            if 'bank_name' in data: programmer.bank_name = data['bank_name']
            if 'iban' in data: programmer.iban = data['iban']
            
            programmer.save()
            
            serializer = ProgrammerSerializer(programmer)
            resp_data = dict(serializer.data)
            resp_data['user_type'] = 'freelancer'
            resp_data['is_superuser'] = user.is_superuser
            return Response(resp_data)
            
        except Programmer.DoesNotExist:
            return Response({'message': 'Profile updated', 'username': user.username})

    try:
        programmer = Programmer.objects.get(user=user)
        serializer = ProgrammerSerializer(programmer)
        data = dict(serializer.data)
        data['user_type'] = 'freelancer'
        data['is_superuser'] = user.is_superuser
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
            'contactClicks': 0,
            'is_superuser': user.is_superuser
        }
        return Response(client_data)



@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def contact_us(request):
    data = request.data
    
    if not data.get('name') or not data.get('message'):
        return Response({'error': 'Name and Message are required'}, status=400)

    try:
        ContactMessage.objects.create(
            name=data.get('name'),
            email=data.get('email'),
            message=data.get('message')
        )
        return Response({'message': 'Message received successfully'})
        
    except Exception as e:
        return Response({'error': str(e)}, status=400)



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
        "hired_projects": ProjectSerializer(hired, many=True, context={'request': request}).data,
        "work_projects": ProjectSerializer(work, many=True, context={'request': request}).data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
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
        amount=data.get('amount', 50.00),
        document=request.FILES.get('document') or data.get('document') 
    )
    return Response(ProjectSerializer(project, context={'request': request}).data, status=201)

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
    if project.client != request.user and project.freelancer.user != request.user:
        return Response({'error': 'Not authorized'}, status=403)
        
    serializer = ProjectSerializer(project, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    try:
        programmer = Programmer.objects.get(user=request.user)
        if project.freelancer != programmer:
            return Response({'error': 'Not authorized'}, status=403)
            
        project.status = 'rejected'
        project.save()
        return Response({'message': 'Project rejected'})
    except Programmer.DoesNotExist:
        return Response({'error': 'Not a freelancer'}, status=403)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def complete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    try:
        programmer = Programmer.objects.get(user=request.user)
        if project.freelancer != programmer:
             return Response({'error': 'Not authorized'}, status=403)
             
        project.status = 'completed'
        project.save()
        return Response({'message': 'Project completed'})
    except Programmer.DoesNotExist:
         return Response({'error': 'Not a freelancer'}, status=403)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def link_github_repo(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if not hasattr(request.user, 'programmer_profile') or project.freelancer != request.user.programmer_profile:
         return Response({'error': 'Only the assigned freelancer can link a repo'}, status=403)

    github_url = request.data.get('github_url')
    if github_url:
        project.github_repo_link = github_url 
        project.save()
        return Response({'message': 'GitHub repository linked successfully'})
    return Response({'error': 'No URL provided'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_project_commits(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.client != request.user and project.freelancer.user != request.user:
        return Response({'error': 'Not authorized'}, status=403)

    if not project.github_repo_link:
        return Response({'error': 'No GitHub repo linked'}, status=404)

    try:
        parts = project.github_repo_link.strip('/').split('/')
        owner = parts[-2]
        repo = parts[-1]
        
        api_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            commits = response.json()[:5] 
            formatted_commits = [{
                'message': c['commit']['message'],
                'author': c['commit']['author']['name'],
                'date': c['commit']['author']['date'],
                'url': c['html_url']
            } for c in commits]
            return Response({'commits': formatted_commits})
        else:
            return Response({'error': 'Could not fetch from GitHub'}, status=response.status_code)
            
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request, project_id):
    try:
        project = get_object_or_404(Project, id=project_id)
        domain_url = 'http://localhost:4200' 
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(project.amount * 100),
                    'product_data': {'name': f"Project: {project.title}"},
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=domain_url + '/dashboard?success=true&session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain_url + '/dashboard?canceled=true',
            metadata={'project_id': project.id, 'client_id': request.user.id}
        )
        return Response({'sessionId': checkout_session.id})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_intent(request, project_id):
    try:
        project = get_object_or_404(Project, id=project_id)
        intent = stripe.PaymentIntent.create(
            amount=int(project.amount * 100),
            currency='usd',
            metadata={
                'project_id': project.id,
                'client_id': request.user.id
            },
            payment_method_types=['card'],
        )
        return Response({'clientSecret': intent.client_secret})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None
    webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '') 

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_payment_success(session)
    
    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        handle_payment_success(intent)

    return HttpResponse(status=200)

def handle_payment_success(obj):
    project_id = obj.get('metadata', {}).get('project_id')
    if project_id:
        try:
            project = Project.objects.get(id=project_id)
            if not project.is_paid:
                project.is_paid = True
                project.status = 'active'
                
                freelancer = project.freelancer
                if hasattr(freelancer, 'balance'):
                    freelancer.balance += project.amount
                    freelancer.save()
                
                project.save()
                print(f"Payment verified for Project {project_id}")
        except Project.DoesNotExist:
            print(f"Project {project_id} not found during webhook processing")

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
    
    freelancer = project.freelancer
    if hasattr(freelancer, 'balance'):
        freelancer.balance += project.amount
        freelancer.save()
    
    project.save()
    return Response({'status': 'Project is now active and freelancer credited'})



class AdminProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser] 
    pagination_class = None 

class AdminDeleteProjectView(generics.DestroyAPIView):
    queryset = Project.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

@api_view(['GET'])
@permission_classes([IsAdminUser]) 
def get_all_messages(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    serializer = ContactMessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_users(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    users = User.objects.all().order_by('-date_joined')
    data = []
    
    for u in users:
        role = 'client'

        if hasattr(u, 'programmer'): 
            role = 'freelancer'
        
        if u.is_superuser or u.is_staff:
            role = 'admin'

        data.append({
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'user_type': role,
            'date_joined': u.date_joined
        })
    return Response(data)