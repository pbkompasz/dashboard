from django.contrib.auth.models import User

def auth(request):
  return {
    'is_logged_in': request.user.is_authenticated,
    'user': User.objects.get(username = request.user),
  }
