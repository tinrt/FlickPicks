from header import *

'''
Author: Tina Nosrati
Last Update: 10/14/2024

Description: 
This script is the usecase of content based movie recommendation.
This will be used in the main dashboard code.

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

##########find_movie_name##########
'''
input:
movie_id --> imdb_id of the movie we are processing

output: name of the movie

Description:
This function will return the name of the movie from
the database using the movie id
'''

def find_movie_name(movie_id):
    try:
        conn,cur=call_database()
        query = "SELECT * FROM movies WHERE imdb_id = %s"        
        cur.execute(query, (str(movie_id),))  
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows,columns=column_names)
        return df.loc[0,'original_title']
    except OperationalError as e:
        print("An operational error occurred:", e)
    except Error as e:
        print("A database error occurred:", e)
    finally:
        cur.close()
        conn.close()


##########find_movie_id##########
'''
input:
name --> name of the movie we are processing

output: imdb_id of the movie

Description:
This function will return the id of the movie from
the database using the movie name
'''
def find_movie_id(name):
    try:
        conn,cur=call_database()
        query = "SELECT * FROM movies WHERE original_title = %s"        
        cur.execute(query, (name,))  
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows,columns=column_names)
        return df.loc[0,'imdb_id']
    except OperationalError as e:
        print("An operational error occurred:", e)
    except Error as e:
        print("A database error occurred:", e)
    finally:
        cur.close()
        conn.close()
    


##########recommend_movies##########
'''
Arguments:
input:

imdb_id --> the id of the movie that we are going to suggest recommendation based on
df --> movies dataframe
cosine_sim --> similarity matrix of the movies used in the recommendation model


Output: a list of recommended movies

Description: 
This function will get the loaded components of the recommendation model
and returns top 5 movies similar to this movie

'''

def recommend_movies(name, df, cosine_sim):
    imdb_id=find_movie_id(name)
    idx = df[df['imdb_id'] == imdb_id].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6] 
    movie_indices = [i[0] for i in sim_scores]
    return df['title'].iloc[movie_indices].tolist()


########## main_program ##########
if __name__=="__main__":
    #model path ~
    model_path = os.path.expanduser('~/content_req_model.pkl') 

    #loading components of the model
    with open(model_path, 'rb') as f:
        df, cosine_sim, tfidf = pickle.load(f) 

    #sample movie id
    #imdb_id = 'tt0403645'   
    name="Jarhead"
    #getting recommendations
    recommendations = recommend_movies(name, df, cosine_sim)
    print(recommendations)

