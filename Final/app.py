'''
Author: Tina Nosrati
Last Update: 12/6/2025

'''

from header import *
from model import get_recommendations, ratings, movies

app = Flask(__name__)

def valid_users():
    # Keep only movies that exist in movies.csv
    valid_movie_ids = set(movies.id.unique())
    ratings_valid = ratings[ratings.movieid.isin(valid_movie_ids)]

    # Users who rated something >=4
    liked = ratings_valid[ratings_valid.rating >= 4]

    # Users that share liked movies with someone else
    user_counts = liked.groupby("movieid")["userid"].count()
    popular_movies = user_counts[user_counts > 1].index.tolist()

    # users with at least one popular movie rated high
    good_users = liked[liked.movieid.isin(popular_movies)]["userid"].unique()

    return sorted(good_users)



@app.route("/", methods=["GET","POST"])
def index():
    recs = []
    dropdown_users = valid_users()   

    if request.method=="POST":
        input_id = request.form.get("user_input") or request.form.get("dropdown_id")

        if input_id and input_id.isdigit():
            user_id = int(input_id)
            recs = get_recommendations(user_id)

    return render_template("index.html", users=dropdown_users, recs=recs)


if __name__=="__main__":
    app.run(debug=True)
