from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserClickCounterSerializer
from music_platform.models import UserClicks
from django.utils.decorators import method_decorator

# Create your views here.

class UserClickCounter(APIView):
    serializer_class = UserClickCounterSerializer
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        validated_data = serializer.validated_data

        inst = UserClicks.objects.filter(user=validated_data["user"], artist=validated_data["artist"])
        if inst:
            inst = inst.first()
            inst.weight += 1
            inst.save()
        else:
            inst = serializer.save()
        return Response(self.serializer_class(instance=inst).data)
