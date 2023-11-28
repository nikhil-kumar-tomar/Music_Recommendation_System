from django.shortcuts import render
from rest_framework import serializers
from music_platform.models import UserClicks
# Create your views here.

class UserClickCounterSerializer(serializers.ModelSerializer):
    weight = serializers.IntegerField(default = 1)

    class Meta:
        model = UserClicks
        fields = "__all__"

