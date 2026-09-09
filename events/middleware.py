
class EventVisitMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print(f"قبل تنفيذ View: {request.method} {request.path}")

        response = self.get_response(request)

        print(f"بعد تنفيذ View: {response.status_code}")

        return response
