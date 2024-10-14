from flask import Flask, render_template, request
from MovieData import get_movie_info
from Review_Summary import generate_movie_summary
from Content_req_test import recommend_movies as content_req
from User_req import recommend_movies as user_req
import os
import pickle

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    try:
        name = None
        info_dict, summary, content_req_list, user_req_list = None, None, None, None

        if request.method == "POST":
            # Get the movie name from the form
            name = request.form.get('name')

            if name:
                # Get movie info
                df = get_movie_info(name)

                # Create dictionary of movie information
                info_dict = df.iloc[0].to_dict()

                # Generate review summary
                summary = generate_movie_summary(name)

                # Content-based recommendation
                content_model_path = os.path.expanduser('~/content_req_model.pkl')
                with open(content_model_path, 'rb') as f:
                    df, cosine_sim, tfidf = pickle.load(f)
                
                content_req_list = content_req(name, df, cosine_sim)

                # User-based recommendation system
                user_req_list = user_req(name)

        return render_template(
            "home.html",
            name=name,
            info=info_dict,
            summary=summary,
            content_req_list=content_req_list,
            user_req_list=user_req_list
        )

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    app.run(debug=True)
