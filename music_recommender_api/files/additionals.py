import pandas as pd
import scipy

import numpy as np
def load_user_artists(user_artists_data, file_type):
    if file_type == "csv":
        user_artists = pd.read_csv(user_artists_data, sep="\t")
    elif file_type == "pd":
        user_artists = user_artists_data
    else:
        return False
    
    user_artists.set_index(["userID", "artistID"], inplace=True)
    
    matrix = scipy.sparse.coo_matrix(
        (
            user_artists.weight.astype(float),
            (
                user_artists.index.get_level_values(0), 
                user_artists.index.get_level_values(1),
            )
            
        )
    )

    return matrix.tocsr()

def count_weight_material(N: int, data: list) -> list[int]:
    int_weights = []
    data = sorted(data, key= lambda x: x["weight"], reverse=True)
    total_plays = sum(map(lambda x: x["weight"], data))
    weight = 1
    itr = 0
    while weight > 0 and itr < len(data):
        current_weight = round(data[itr]["weight"] / total_plays, 3)
        if weight < current_weight:
            current_weight = weight
        
        weight -= round(current_weight, 3)

        int_weights.append(current_weight)
        itr += 1

    int_weights = [int(N * weight) for weight in int_weights if int(N * weight) != 0]
    
    if sum(int_weights) < N and len(int_weights) != 0:
        int_weights[0] = int_weights[0] + (N - sum(int_weights))

    return int_weights, data
