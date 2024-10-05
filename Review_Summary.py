from header import *

'''
Author: Tina Nosrati
Last Update: 10/5/2024

Description: 
This script will summarize movie reviews for a selected movie.
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


##########get_reviews_for_imdb_id##########
'''
Arguments:
input:
imdb_id --> id of the selected movie

Output: A dataframe containing reviews for the selected movie

Description: 
This function will return a dataframe of reviews for a selected movie from the database

'''
def get_reviews_for_imdb_id(imdb_id):
    try:
        conn, cur = call_database()
        query = "SELECT * FROM reviews WHERE imdb_id = %s"        
        cur.execute(query, (imdb_id,))       
        rows = cur.fetchall()     
        column_names = [desc[0] for desc in cur.description]     
        df = pd.DataFrame(rows, columns=column_names)     
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
if __name__=="__main__":
    # get rating data
    df=call_database()
    imdb_id="tt0113228"
    reviews=get_reviews_for_imdb_id(imdb_id)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    full_text = ' '.join(reviews['review'].tolist())
    print(summarizer(full_text, max_length=130, min_length=30, do_sample=False))

