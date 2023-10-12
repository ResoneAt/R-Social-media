from django.utils.deprecation import MiddlewareMixin


class CustomMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from accounts.models import User
        users = User.objects.all().order_by('?')
        request.project_context = {'users': users}
        response = self.get_response(request)
        return response


