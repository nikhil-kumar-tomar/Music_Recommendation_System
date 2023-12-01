import implicit
import pandas as pd
import numpy
from .additionals import load_user_artists, count_weight_material


class Recommender:
    def __init__(self, als_model):
        self.als_model = als_model

    def similar_items(self, artist_id: int, n: int):
        artist_ids, scores = self.als_model.similar_items(artist_id, N=n)
        return artist_ids, scores

loaded = False
def load():
    global global_user_artists_matrix, recommend_obj, loaded
    als_model = implicit.als.AlternatingLeastSquares()  
    als_model = als_model.load("model_best")
    recommend_obj = Recommender(als_model)
    global_user_artists_matrix = load_user_artists("lastfmdata/user_artists.dat", "csv")
    loaded = True
    
def recommend_songs(data: list[dict], N: int):
    
    if loaded == False:
        load()
    count_weights, data = count_weight_material(N=N, data=data)
    total_artists_info = []
    for itr in range(len(count_weights)):
        artists_info, scores = recommend_obj.similar_items(data[itr]["artist_id"],
                                                           n=count_weights[itr]
                                                           )
        total_artists_info.extend(artists_info)

    total_artists_info = numpy.array(total_artists_info)
    total_artists_info = numpy.unique(total_artists_info).tolist()
    return total_artists_info
