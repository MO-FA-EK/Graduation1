import time
import logging

logger = logging.getLogger(__name__)

class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Start measuring
        start_time = time.time()

        # Process the request
        response = self.get_response(request)

        # End measuring
        duration = round((time.time() - start_time) * 1000, 2)

        # Prepare log entry
        method = request.method
        path = request.get_full_path()
        status_code = response.status_code
        user = (
            request.user.username 
            if hasattr(request, "user") and request.user.is_authenticated 
            else "Anonymous"
        )

        logger.info(
            f"[API LOG] {method} {path} → {status_code} | {duration} ms | User: {user}"
        )

        return response
