from django.contrib.sessions.models import Session

class ClearSessionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        Session.objects.all().delete()  # Clear all sessions

    def __call__(self, request):
        response = self.get_response(request)
        return response