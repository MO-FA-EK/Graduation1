from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


def custom_auth_exception_handler(exc, context):
    """
    Wrap DRF + SimpleJWT errors in cleaner, frontend-friendly messages.
    """

    response = exception_handler(exc, context)

    # If DRF didn't handle it, just return as-is.
    if response is None:
        return response

    # IMPORTANT: check token errors (InvalidToken, TokenError) BEFORE AuthenticationFailed,
    # because InvalidToken is a subclass of AuthenticationFailed.
    if isinstance(exc, (InvalidToken, TokenError)):
        response.data = {"detail": "Token is invalid or has expired."}

    elif isinstance(exc, AuthenticationFailed):
        # This mainly covers wrong username/password on login
        response.data = {"detail": "Invalid username or password."}

    elif isinstance(exc, NotAuthenticated):
        response.data = {"detail": "Authentication credentials were not provided."}

    return response
