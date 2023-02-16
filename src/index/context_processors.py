from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

def auth(request):
  return {
    'is_logged_in': request.user.is_authenticated,
    'user': request.user
  }
