from header import *

'''
Author: Tina Nosrati
Last Update: 10/1/2024

Description: 
This script will develop the content based recommendation model.
'''




##########call_database##########
'''
Arguments:
input:

Output: connection and cursor to work with database

Description: 
This function will connect to database

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



##########get_movie_data##########
'''
Arguments:
input:

Output: A dataframe containing movies in the database

Description: 
This function will return a dataframe of movies from the database

'''
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



##########clean_data##########
'''
Arguments:
input: A string x

Output: cleaned version of the input string

Description: 
This function will clean an input string by removing these characters ([,],',{,})

'''
def clean_data(x):
    if isinstance(x, str):
        return x.replace("[", "").replace("]", "").replace("'", "").replace("{", "").replace("}", "")
    else:
        return ''


##########prep_data##########
'''
Arguments:
input: A dataframe df

Output: A dataframe df

Description: 
This function will perform data prepration on the attributes of the dataframe
that is going to be used in our recommendation model. This function will also add
a "combined_features" column to the dataset

'''
def prep_data(df):
    df['genres'] = df['genres'].apply(clean_data)
    df['spoken_languages'] = df['spoken_languages'].apply(clean_data)
    df['overview'] = df['overview'].fillna('')
    df['combined_features'] = df['genres'] + ' ' + df['spoken_languages'] + ' ' + df['overview']
    return df


##########get_recommendations##########
'''
Arguments:
input:
imdb_id --> id of the movie that we are going to get recommendation for
cosine_sim --> the cosine similarity matrix

Output: A ist of imdb_id as the recommendation list

Description: 
This function will use the cosine similarity matrix to score and sort movies
and create a recommendation list for the input movie

'''
def get_recommendations(imdb_id, cosine_sim):
    idx = df.index[df['imdb_id'] == imdb_id].tolist()[0]    
    sim_scores = list(enumerate(cosine_sim[idx]))    
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)    
    sim_scores = sim_scores[1:6]    
    movie_indices = [i[0] for i in sim_scores]    
    return df['imdb_id'].iloc[movie_indices].values


##########get_recommendations##########
'''
Arguments:
input:
imdb_id --> id of the movie that we are going to get recommendation for

Output: A list of movies in the same  collection with this movie

Description: 
This function will make sure that we are recommending all the movies in the same collection
if a movie is in a collection

'''
def recommend_collection(imdb_id):
    movie = df[df['imdb_id'] == imdb_id]
    if not movie['belongs_to_collection'].isnull().values[0]:
        collection_name = movie['belongs_to_collection'].values[0]
        collection_movies = df[df['belongs_to_collection'] == collection_name]
        return collection_movies['imdb_id'].values
    else:
        return None


##########get_recommendations##########
'''
Arguments:
input:
imdb_id --> id of the movie that we are going to get recommendation for

Output: A list of recommended movies or calling 'get_recommendations' function 

Description: 
This function will return the rest of the movies in the collection if a movie blongs to
a collection of will call the 'get_recommendations' function to create recomendation based on 
similarity

'''
def recommend_movies(imdb_id):
    collection_recommendations = recommend_collection(imdb_id)
    if collection_recommendations is not None:
        return collection_recommendations[:6]  
    else:
        return get_recommendations(imdb_id,cosine_sim)


# main program
if __name__=="__main__":
    
    # getting movies
    df=get_movie_data()

    # preparing data
    df=prep_data(df)

    # set TFIDF for text processing on movie reviews
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])

    # set cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    df = df.reset_index()

    # save recommendation model
    output_model_path = os.path.expanduser('~/content_req_model.pkl')
    with open(output_model_path, 'wb') as f:
        pickle.dump((df, cosine_sim, tfidf), f)
    print(f"Model saved to {output_model_path}")

    # test
    imdb_id = 'tt0113189' 
    recommendations = recommend_movies(imdb_id)
    print(recommendations)