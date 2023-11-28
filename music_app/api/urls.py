from django.urls import path
from .views import UserClickCounter
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('add_user_click/', UserClickCounter.as_view(), name="user-click-add")
]
