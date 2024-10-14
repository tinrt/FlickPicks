from header import *

'''
Author: Tina Nosrati
Last Update: 10/13/2024

Description: 
This script will prepare general movie information
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


##########get_movie_info##########
'''
Arguments:
input:
imdb_id --> id of the selected movie

Output: A dataframe containing information for the selected movie

Description: 
This function will return a dataframe of information for a selected
movie from the database.
'''

def get_movie_info(imdb_id):
    try:
        conn, cur = call_database()
        query = "SELECT * FROM movies WHERE imdb_id = %s"        
        cur.execute(query, (imdb_id,))       
        rows = cur.fetchall()     
        column_names = [desc[0] for desc in cur.description]     
        df = pd.DataFrame(rows, columns=column_names) 
        df = df.sample(frac=1).reset_index(drop=True) 
        return df
    
    except OperationalError as e:
        print("An operational error occurred:", e)
    except Error as e:
        print("A database error occurred:", e)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# main program
if __name__ == "__main__":
    # get movie data
    imdb_id = "tt0113987"
    df = get_movie_info(imdb_id)
    info_dict = df.iloc[0].to_dict()
    print(info_dict)
    