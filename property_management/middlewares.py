from rest_framework_simplejwt import authentication


class JWTMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        auth = authentication.JWTAuthentication().authenticate(request)
        if auth:
            request.user = auth[0]
