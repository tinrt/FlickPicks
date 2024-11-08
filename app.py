from flask import Flask, render_template, request
from MovieData import get_movie_info,clean_dictionary
from Review_Summary import generate_movie_summary
from Content_req_test import recommend_movies as content_req
from User_req import recommend_movies as user_req
import os
import pickle

app = Flask(__name__)

# Function to correct user input
def correct_movie_name(movie_name):
    return movie_name.title()

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        name = None
        info_dict, summary, content_req_list, user_req_list = None, None, None, None

        if request.method == 'POST':
            # Get the movie name from the form
            name = request.form.get('name')

            if name:
                # Correct the movie name format
                name = correct_movie_name(name)
                # Get movie info
                df = get_movie_info(name)

                # Create dictionary of movie information
                info_dict = df.iloc[0].to_dict()
                info_dict=clean_dictionary(info_dict)

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
        return render_template('error.html')

# Custom error handler for 404 (Page Not Found)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

# Custom error handler for 500 (Internal Server Error)
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
