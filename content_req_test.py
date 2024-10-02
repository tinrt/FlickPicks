from header import *

def recommend_movies(imdb_id, df, cosine_sim):
    idx = df[df['imdb_id'] == imdb_id].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11] 
    movie_indices = [i[0] for i in sim_scores]
    return df['title'].iloc[movie_indices]

if __name__=="__main__":
    model_path = os.path.expanduser('~/content_req_model.pkl')
    with open(model_path, 'rb') as f:
        df, cosine_sim, tfidf = pickle.load(f)
    imdb_id = 'tt0403645'  
    recommendations = recommend_movies(imdb_id, df, cosine_sim)
    print(recommendations)