import os
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
@permission_classes([AllowAny])
def ai_chat(request):
    try:
        api_key = os.getenv("DEEPSEEK_API_KEY")

        user_message = request.data.get("message", "").strip()
        if not user_message:
            return Response(
                {"error": "Message is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        system_prompt = (
            "You are an AI assistant for the SoftwJob platform. "
            "Guide users (clients, freelancers, admins) on how to use the website. "
            "Do not ask for passwords or sensitive information."
        )

        if not api_key:
            return Response({
                "reply": fallback_response(user_message)
            }, status=status.HTTP_200_OK)

        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            },
            timeout=20
        )

        data = response.json()

        if "error" in data:
            return Response({
                "reply": fallback_response(user_message)
            }, status=status.HTTP_200_OK)

        reply = data["choices"][0]["message"]["content"]
        return Response({"reply": reply}, status=status.HTTP_200_OK)

    except Exception as e:
        print("AI ERROR >>>", repr(e))
        return Response({
            "reply": fallback_response(user_message)
        }, status=status.HTTP_200_OK)


def fallback_response(message: str) -> str:
    """
    Fallback logic when AI API is unavailable.
    """

    msg = message.lower()

    if "hire" in msg or "client" in msg:
        return (
            "To hire a freelancer, go to the Services page, browse available freelancers, "
            "view their profiles, and use the contact option to start communication."
        )

    if "freelancer" in msg or "work" in msg:
        return (
            "Freelancers can manage their profile, view assigned projects, "
            "and track ongoing work from the Dashboard section."
        )

    if "login" in msg or "register" in msg:
        return (
            "You can register or log in using the authentication pages accessible "
            "from the navigation bar at the top of the website."
        )

    if "admin" in msg:
        return (
            "Administrators can access the Admin Panel to manage users, "
            "freelancers, and platform content."
        )

    return (
        "I can help you navigate the SoftwJob platform. "
        "Please explore the Home, Services, or Dashboard pages for more information."
    )
