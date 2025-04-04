import time
class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print('Middleware initialized')
    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        print(f'Request took {duration:.2f} seconds')
        return response