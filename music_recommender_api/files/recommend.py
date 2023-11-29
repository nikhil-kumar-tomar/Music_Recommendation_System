import implicit
import scipy
import pandas as pd
import numpy
from .additionals import load_user_artists
# def load_user_artists(user_artists_file):
#     user_artists = pd.read_csv(user_artists_file, sep="\t")
#     user_artists.set_index(["userID", "artistID"], inplace=True)
    
#     matrix = scipy.sparse.coo_matrix(
#         (
#             user_artists.weight.astype(float),
#             (
#                 user_artists.index.get_level_values(0), 
#                 user_artists.index.get_level_values(1),
#             )
#         )
#     )

#     return matrix.tocsr()

def count_weight_material(count: int, N: int) -> list[int]:
    int_weights = []
    if count == 3:
        int_weights = [int(N * 0.6), int(N * 0.3), int(N * 0.1)]
    elif count == 2:
        int_weights = [int(N * 0.8), int(N * 0.2)]
    else:
        int_weights = [int(N * 1)]
    
    int_weights = [x for x in int_weights if x != 0]


    if sum(int_weights) < N and len(int_weights) != 0:
        int_weights[0] = int_weights[0] + (N - sum(int_weights))
    elif len(int_weights) == 0:
        int_weights.append(N)

    return int_weights

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

    data = sorted(data, key= lambda x: x["weight"], reverse=True)
    count = len(data)
    if count > 3:
        raise {"detail":"Most weighted 3 entries are allowed only"}

    count_weights = count_weight_material(count, N)
    # filter_out_items = [x["artist_id"] for x in data]
    total_artists_info = []

    for itr in range(len(count_weights)):
        artists_info, scores = recommend_obj.similar_items(data[itr]["artist_id"],
                                                           n=count_weights[itr],
                                                        #    filter_items=filter_out_items
                                                           )
        total_artists_info.extend(artists_info)

    total_artists_info = numpy.array(total_artists_info)
    total_artists_info = numpy.unique(total_artists_info).tolist()
    return total_artists_info
