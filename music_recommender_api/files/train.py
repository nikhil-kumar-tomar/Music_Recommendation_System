import implicit
import scipy
import pandas as pd
from additionals import load_user_artists

user_artists = load_user_artists("lastfmdata\\user_artists.dat", "csv") # <- Thisf our matrix basically, User is vertical and items(artists) is horizontal 

als_model = implicit .als.AlternatingLeastSquares(
    factors=20, iterations=10, regularization=0.01
)

als_model.fit(user_artists)

als_model.save("model_prac")