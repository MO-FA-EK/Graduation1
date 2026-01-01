import os
import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.conf import settings

def get_gemini_model():
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

SYSTEM_PROMPT = """
You are the AI Assistant for SoftwJob, a freelancing platform.
Your role is to guide users (Clients, Freelancers, Administrators) on how to use the platform.
You answer questions related to Navigation, Account usage, Projects, Dashboards, and GitHub linking.
You DO NOT perform system actions, access sensitive data (passwords, payments), or reset accounts.
Refuse to answer questions unrelated to SoftwJob platform usage.
Keep responses concise, friendly, and step-based if offering instructions.
"""

class AIChatView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user_message = request.data.get('message')
        user_role = request.data.get('role', 'guest')
        current_page = request.data.get('current_page', '/')

        if not user_message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        model = get_gemini_model()
        if not model:
            return Response({"error": "AI Service unavailable (API Key missing)"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            full_prompt = f"{SYSTEM_PROMPT}\n\n"
            full_prompt += f"User Role: {user_role}\n"
            full_prompt += f"Current Page: {current_page}\n"
            full_prompt += f"User Request: {user_message}\n"

            response = model.generate_content(full_prompt)
            
            if not response.text:
                return Response({"reply": "I'm sorry, I couldn't generate a response for that."}, status=status.HTTP_200_OK)

            return Response({"reply": response.text})

        except Exception as e:
            print(f"AI Error: {str(e)}")
            return Response({"error": "Unable to process your request at this time."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
