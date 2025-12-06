'''
Author: Tina Nosrati
Last Update: 12/6/2025

'''

from header import *


movies = pd.read_csv("data\\movies_metadata.csv")
ratings = pd.read_csv("data\\ratings.csv")



def clean_genres(genre_str):
    """Convert TMDB JSON-like list to clean string 'Action, Drama'"""
    try:
        genre_list = ast.literal_eval(genre_str)
        return ", ".join([g['name'] for g in genre_list])
    except:
        return genre_str  



def get_recommendations(user_id, top_n=5, similarity_threshold=0.5):

    user_ratings = ratings[ratings["userid"] == user_id]
    high_rated_movies = user_ratings[user_ratings["rating"] >= 4]["movieid"].tolist()

    if len(high_rated_movies) == 0:
        return ["User has no high ratings — cannot recommend."]

    similar_users = ratings[
        (ratings["movieid"].isin(high_rated_movies)) &
        (ratings["rating"] >= 4) &
        (ratings["userid"] != user_id)
    ]["userid"].unique()

    if len(similar_users) == 0:
        return ["No similar users found."]

    recommendations = ratings[
        (ratings["userid"].isin(similar_users)) &
        (ratings["rating"] >= 4) &
        (~ratings["movieid"].isin(high_rated_movies))
    ]["movieid"].value_counts().head(top_n).index.tolist()

    # Get movies
    recommended_movies = movies[movies["id"].isin(recommendations)].copy()

    # Clean genre formatting
    recommended_movies["genres"] = recommended_movies["genres"].apply(clean_genres)

    # Replace popularity with rating 1–5
    recommended_movies["popularity"] = recommended_movies["vote_average"]

    return recommended_movies.to_dict('records')

