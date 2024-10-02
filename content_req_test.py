from header import *

'''
Author: Tina Nosrati
Last Update: 10/1/2024

Description: 
This script is the usecase of content based movie recommendation.
This will be used in the main dashboard code.

'''


##########get_movie_reviews##########
'''
Arguments:
input:

imdb_id --> the id of the movie that we are going to suggest recommendation based on
df --> movies dataframe
cosine_sim --> similarity matrix of the movies used in the recommendation model


Output: a list of recommended movies

Description: 
This function will get the loaded components of the recommendation model
and returns top 10 movies simmilar to this movie

'''

def recommend_movies(imdb_id, df, cosine_sim):
    idx = df[df['imdb_id'] == imdb_id].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11] 
    movie_indices = [i[0] for i in sim_scores]
    return df['title'].iloc[movie_indices]


########## main_program ##########
if __name__=="__main__":
    #model path ~
    model_path = os.path.expanduser('~/content_req_model.pkl') 

    #loading components of the model
    with open(model_path, 'rb') as f:
        df, cosine_sim, tfidf = pickle.load(f) 

    #sample movie id
    imdb_id = 'tt0403645'   

    #getting recommendations
    recommendations = recommend_movies(imdb_id, df, cosine_sim)
    print(recommendations)