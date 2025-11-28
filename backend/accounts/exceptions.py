from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response

def custom_auth_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return response

    data = response.data

    # -------- Token errors (refresh / validate-token) --------
    if isinstance(data, dict) and data.get("code") == "token_not_valid":
        return Response(
            {"detail": "Your session expired. Please log in again."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # SimpleJWT sometimes returns token errors like this:
    if isinstance(data, dict) and "detail" in data and "token" in str(data["detail"]).lower():
        return Response(
            {"detail": "Invalid token. Please log in again."},
            status=response.status_code
        )

    # -------- Invalid login credentials --------
    if data.get("detail") == "No active account found with the given credentials":
        response.data = {"detail": "Incorrect username or password."}
        return response

    # -------- Missing Authorization header --------
    if data.get("detail") == "Authentication credentials were not provided.":
        response.data = {"detail": "Login required."}
        return response

    # Default: keep original error
    return response

