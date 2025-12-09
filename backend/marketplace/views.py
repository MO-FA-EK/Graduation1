from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Programmer
from .serializers import ProgrammerSerializer

# LIST PROGRAMMERS
@api_view(["GET"])
def programmer_list(request):
    programmers = Programmer.objects.all()
    serializer = ProgrammerSerializer(programmers, many=True)
    return Response(serializer.data)

# PROGRAMMER DETAILS
@api_view(["GET"])
def programmer_detail(request, id):
    try:
        programmer = Programmer.objects.get(id=id)
    except Programmer.DoesNotExist:
        return Response({"error": "Not found"}, status=404)
    
    serializer = ProgrammerSerializer(programmer)
    return Response(serializer.data)

# RATE PROGRAMMER
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def rate_programmer(request, id):
    try:
        programmer = Programmer.objects.get(id=id)
    except Programmer.DoesNotExist:
        return Response({"error": "Programmer not found"}, status=404)

    rating = request.data.get("rating")
    if rating is None:
        return Response({"error": "Rating is required"}, status=400)

    programmer.rating = rating
    programmer.review_count += 1
    programmer.save()

    return Response({"message": "Rating saved", "rating": programmer.rating})

# USER PROFILE
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_profile(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })
