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

def combined_df(df1: pd, df2: pd) -> pd:
    result = pd.concat([df1, df2], ignore_index=True)
    return result
