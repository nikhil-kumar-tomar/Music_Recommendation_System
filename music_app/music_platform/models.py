from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class custom_user(AbstractUser):
    id = models.AutoField(primary_key=True)
    email=models.EmailField(unique=True)

class music_uploads_model(models.Model):
    GENRE_CHOICES = [
        ("disco","Disco"),
        ("funk","Funk"),
        ("rock","Rock"),
        ("blues","Blues"),
        ("rapping","Rapping"),
    ]
    date_time=models.DateTimeField(auto_now_add=True)
    music_name=models.CharField(max_length=400)
    music_file=models.FileField(upload_to="music/")
    music_type=models.CharField(max_length=10)
    music_genre = models.CharField(choices=GENRE_CHOICES, max_length=10)
    owner_email=models.ForeignKey(custom_user,to_field="email",on_delete=models.CASCADE,unique=False)
    def __str__(self):
        return f"{self.music_name} | {self.music_type} belong to {self.owner_email}"

class protected_accessors(models.Model):
    music_id=models.ForeignKey(music_uploads_model,to_field="id",on_delete=models.CASCADE,unique=False)
    email=models.ForeignKey(custom_user,to_field="email",on_delete=models.CASCADE,unique=False)
    def __str__(self):
        return f"{self.email}->{self.music_id}"
    class Meta:
        unique_together=("music_id","email")

class Artists(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(300)
    url = models.URLField(null=True)
    picture_url = models.URLField(null=True)

class UserClicks(models.Model):
    user = models.ForeignKey(custom_user, to_field="id", on_delete=models.CASCADE, related_name="clicks")
    artist = models.ForeignKey(Artists, to_field="id", on_delete=models.CASCADE, related_name="plays")
    weight = models.IntegerField()
    
