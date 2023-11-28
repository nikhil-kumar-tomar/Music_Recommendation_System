from fastapi import FastAPI
from files.recommend import recommend_songs
from files.additionals import load_user_artists
from serializers import GetRecommendsSerializer
app = FastAPI()

@app.post("/get_recommends/")
def get_recommends(params: GetRecommendsSerializer):
    artists = recommend_songs(data=params.data, N=params.N)
    return artists

