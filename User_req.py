from header import *

'''
Author: Tina Nosrati
Last Update: 10/5/2024

Description: 
This script will develop the user based recommendation model.
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


##########get_user_data##########
'''
Arguments:
input:

Output: A dataframe containing user movie raitings in the database

Description: 
This function will return a dataframe of user movie raitings from the database

'''
def get_user_data():
    try:
        conn,cur=call_database()
        query = "SELECT * FROM ratings"
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


##########get_high_ratings_userid##########
'''
Arguments:
input:
df --> The input dataframe containing columns ['userid', 'movie_id', 'rating', 'timestamp']
movie_id --> id of the movie to filter by
rating_threshold --> The minimum rating considered as 'high'. Default is 3.0

Output: A list of user IDs who rated the specified movie above the threshold

Description: 
This function will Filters the dataframe to return a list of user id who rated a specific movie above the given rating threshold

'''

def get_high_ratings_userid(df, movie_id, rating_threshold=3.0):
    filtered_df = df[(df['movie_id'] == str(movie_id)) & (df['rating'] > rating_threshold)]
    
    return filtered_df['userid'].tolist()



##########get_high_rated_movie_ids##########
'''
Arguments:
input:
df --> The input dataframe containing columns ['userid', 'movie_id', 'rating', 'timestamp']
exclude_movie_id --> (Optional) A movie id to exclude
rating_threshold --> The minimum rating considered as 'high'. Default is 4.0

Output: A list of the top 5 movie IDs

Description: 
This function will Filters the dataframe to return the top 5 other movies highly rated by a given list of users

'''
def get_high_rated_movie_ids(df, user_ids, exclude_movie_id=None, rating_threshold=4.0):
    filtered_df = df[(df['userid'].isin(user_ids)) & (df['rating'] > rating_threshold)]

    if exclude_movie_id:
        filtered_df = filtered_df[filtered_df['movie_id'] != exclude_movie_id]
    
    filtered_df = filtered_df.sort_values(by='rating', ascending=False)
    
    return filtered_df['movie_id'].head(5).tolist()



# main program
if __name__=="__main__":
    # get rating data
    df=get_user_data()

    #test
    movie_id=100

    #get recommedation
    df_similar_users=get_high_ratings_userid(df,movie_id)
    top_5=get_high_rated_movie_ids(df, df_similar_users)
    print(top_5)