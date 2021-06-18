from rest_framework_simplejwt import authentication
from django.contrib.auth.models import AnonymousUser


class JWTMiddleware:
    """
    Simple JWT does not fill 'request.user'. For easier access to user
    information in the views, this middleware fills 'request.user'.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            auth = authentication.JWTAuthentication().authenticate(request)
            if auth:
                request.user = auth[0]
        except:
            request.user = AnonymousUser
