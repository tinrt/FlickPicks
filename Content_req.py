from header import *

'''
Author: Tina Nosrati
Last Update: 10/1/2024

Description: 
This script will develop the content based recommendation model.
'''

def call_database():
    conn = psycopg2.connect(
    host="localhost",
    dbname="moviedata",
    user="postgres",
    password="1234",
    port=5432)
    cur = conn.cursor()
    return conn,cur

def get_movie_data():
    try:
        conn,cur=call_database()
        query = "SELECT * FROM movies"
        cur.execute(query)
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows,columns=column_names)
        return df
    except OperationalError as e:
        print("An operational error occurred:", e)
    except Error as e:
        print("A database error occurred:", e)
    finally:
        cur.close()
        conn.close()

def clean_data(x):
    if isinstance(x, str):
        return x.replace("[", "").replace("]", "").replace("'", "").replace("{", "").replace("}", "")
    else:
        return ''

def prep_data(df):
    df['genres'] = df['genres'].apply(clean_data)
    df['spoken_languages'] = df['spoken_languages'].apply(clean_data)
    df['overview'] = df['overview'].fillna('')
    df['combined_features'] = df['genres'] + ' ' + df['spoken_languages'] + ' ' + df['overview']
    return df

def get_recommendations(imdb_id, cosine_sim):
    idx = df.index[df['imdb_id'] == imdb_id].tolist()[0]    
    sim_scores = list(enumerate(cosine_sim[idx]))    
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)    
    sim_scores = sim_scores[1:6]    
    movie_indices = [i[0] for i in sim_scores]    
    return df['imdb_id'].iloc[movie_indices].values

def recommend_collection(imdb_id):
    movie = df[df['imdb_id'] == imdb_id]
    if not movie['belongs_to_collection'].isnull().values[0]:
        collection_name = movie['belongs_to_collection'].values[0]
        collection_movies = df[df['belongs_to_collection'] == collection_name]
        return collection_movies['imdb_id'].values
    else:
        return None

def recommend_movies(imdb_id):
    collection_recommendations = recommend_collection(imdb_id)
    if collection_recommendations is not None:
        return collection_recommendations[:6]  
    else:
        return get_recommendations(imdb_id,cosine_sim)


if __name__=="__main__":
    df=get_movie_data()
    df=prep_data(df)
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    df = df.reset_index()
    output_model_path = os.path.expanduser('~/content_req_model.pkl')
    with open(output_model_path, 'wb') as f:
        pickle.dump((df, cosine_sim, tfidf), f)
    print(f"Model saved to {output_model_path}")


    imdb_id = 'tt0113189' 
    recommendations = recommend_movies(imdb_id)
    print(recommendations)