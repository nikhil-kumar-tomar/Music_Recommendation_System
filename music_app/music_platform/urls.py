# Configure App urls here
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("home/",views.home),
    path("",views.root),
    path("registration/",views.registration),
    path('login/',views.logins),
    path("logout/",views.logouts),
    # path("upload_music/",views.music_upload),
    # path("upload_music_protected_access_allowed_<int:music_id>/",views.music_upload_protected_allows)
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)