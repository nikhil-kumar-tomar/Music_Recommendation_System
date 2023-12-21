# Music Recommendation System
This repository contains the source code for a Music Recommendation System, designed to provide personalized artist recommendations based on user listening patterns. The system integrates with the Spotify API, utilizes a Celery-based asynchronous task processing system, incorporates a Alternating Least Squares ML model for recommendation calculations, and employs Redis caching for improved performance.

## Technologies Used
- Django
- Celery
- Redis
- FastAPI
- Django Rest Framework
- PostgreSQL

## Architecture

### User Initialization

When a new user registers, the system generates random artist suggestions. The Spotify API is then used to fetch the most popular songs of these suggested artists.

### User Interaction Tracking

The system tracks user interactions, such as song plays, against the `artist_id` in the database. After every 5 songs a user listens to, the web app asynchronously requests Celery workers to recalculate recommendations for the user and the cache is updated accordingly.

### Celery Workers Processing

Celery workers query user information from the database, including play counts for different artists. This information is formatted as `{artist_id: 5, plays: 10}` and is used as input for the ML service.

### ML Service Integration

The ML service, exposed via an API, receives user play counts and calculates weights for each artist, indicating how many similar artists to a particular artist should be returned. The ML service then returns recommended `artist_ids` based on the user's listening patterns.

### Fetching Artist Information

The web application retrieves artist names corresponding to the recommended `artist_ids` from the database.

### Spotify API Integration

The Spotify search API is used to find the most popular song of each recommended artist using their names.

### Caching in Redis

After fetching information like `song_name`, `image`, `URL`, and `artist_name`, the data is cached in a Redis database. Subsequent requests to the web app are served directly from the Redis cache, reducing latency.


## System Design
![ScreenShot](/images/Music_Recommendation_System_Systems_Design.png)

## Database Design
![ScreenShot](/images/Music_Recommendation_System_Database_ER_Diagram.png)

## Machine Learning Model in the Music Recommendation System

The machine learning model employed in the Music Recommendation System is designed to provide personalized artist recommendations based on user listening patterns. Instead of directly using users for recommendations, the model focuses on the playcounts of users for specific artists. The goal is to calculate weights and determine the similarity between artists, ultimately generating a list of recommended artists.

### Training Data
The dataset used for training is [lastfm dataset](http://millionsongdataset.com/lastfm/) 
The model is trained on data structured as a matrix like below:

```json
|            | Artist_1 | Artist_2 | Artist_3 |
|------------|----------|----------|----------|
| User_1     | 2        | 5        | 8        |
| User_2     | 4        | 1        |          |
| User_3     | 6        | 3        | 9        |
```

The data input to recommendations looks like below and is sent by the celery workers directly for a specific user.

```json
[
    {
        "artist_id": 9,
        "plays": 10
    },
    {
        "artist_id":5,
        "plays":5
    }
    ...
]
```

### Weight Calculation
The entries are not directly sent to ML Model, Weights for each artist has to be found.
**Weight here refers to the percentage of NUMBER_OF_ARTISTS that a particular artist will fill** 
the NUMBER_OF_ARTISTS is defined in .env file and it represents the total recommendations of artists to be returned from the ML model.**

#### Formula for Weights
\[
\text{Weight} = \left( \frac{\text{plays}}{\text{total\_plays}} \right)
\]

\[
\text{total\_plays} = \sum_{i \in \text{artist\_ids}} \text{artist\_plays}_i
\]

#### Example
*Weight for artist 9*

```
plays for artist_9 = 10
total_plays = 15

weight = 10 / 15 ~ 0.66 or 66%

NUMBER_OF_ARTISTS = 100
artists similar to artist_9 will take 66 entries in the list.
other 34 entires, will be taken by other artists based on their weight.
```

### ML Working
The weight array is then converted to form a number_of_entries for each artist array. for conversion we use `entry_for_artist_i = INT(weight * NUMBER_OF_ARTISTS)`. This is done for every artist in artist objects array and a entries array is formed.

both the objects array of artists as well as number_of_entries array is sorted into descending order based on their plays.

from above example
```
artist_objects_descending = [
    {
        "artist_id": 9,
        "plays": 10
    },
    {
        "artist_id":5,
        "plays":5
    }
    ...
]

number_of_entires_decending = [
    66,
    34
]
```

Finally all of this information is given to the Alternating Least Squares model one by one to generate similar items, the number_of_entries for a particular artist are also provided to yield only a particular number of  similar artist_ids.

All of the above ids are placed into a global array which is finally returned by the API.





