from django.contrib.auth.backends import ModelBackend
from police.models import Police

class MatriculaBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Police.objects.get(matricula=username)
        except Police.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return Police.objects.get(pk=user_id)
        except Police.DoesNotExist:
            return None
        
class NameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Police.objects.get(name=username)
        except Police.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return Police.objects.get(pk=user_id)
        except Police.DoesNotExist:
            return None
