import time

class RequestTimeLoggingMiddleware:
    """
    Middleware to log the time taken to process each request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        print(f"Request processed in {duration:.2f} seconds")
        return response