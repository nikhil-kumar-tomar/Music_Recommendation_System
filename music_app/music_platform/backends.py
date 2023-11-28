from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

user_model=get_user_model()
class email_backend(ModelBackend):
    def authenticate(self,request,username=None,password=None,**kwargs):
        try:
            user=user_model.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except user_model.DoesNotExist:
            user_model().set_password(password)
            return
        except user_model.MultipleObjectsReturned:
            user=user_model.objects.filter(Q(username__iexact=username) | Q(email__iexact=username).orderby('id'.first()))
        if user.check_password(password) and self.user_can_authenticate(user):
            return user