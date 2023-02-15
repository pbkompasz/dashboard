from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

def auth(request):
  try:
    user = User.objects.get(username = request.user),
  except ObjectDoesNotExist:
    user = None
  return {
    'is_logged_in': request.user.is_authenticated,
    'user': user
  }
