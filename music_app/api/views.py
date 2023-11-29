from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserClickCounterSerializer
from music_platform.models import UserClicks
from music_platform.miscellaneous import set_user_plays, get_user_choices
from music_platform.celery_tasks import music_cacher
from .models import PreviousMLUse
from django.conf import settings
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
        
        previous_play_obj = PreviousMLUse.objects.filter(user_id=validated_data["user"]).first()
        
        user_liked_songs = get_user_choices(user_id=validated_data["user"])
        
        total_plays = sum(map(lambda x: x["weight"] ,user_liked_songs))

        if previous_play_obj and total_plays >= 5 + previous_play_obj.total_plays:
            
            ml_data = {
                "data":user_liked_songs,
                "N":int(settings.NUMBER_OF_ARTISTS) 
            }

            music_cacher.delay(ml_data=ml_data, user_id=validated_data["user"].id, NUMBER_OF_SONGS_PER_ARTIST=int(settings.NUMBER_OF_SONGS_PER_ARTIST))
            
            set_user_plays(validated_data["user"].id, user_liked_songs)
        return Response(self.serializer_class(instance=inst).data)
