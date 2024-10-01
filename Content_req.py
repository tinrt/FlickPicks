from header import *

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
        query = "SELECT * FROM movies LIMIT 5"
        cur.execute(query)
        rows = cur.fetchall()
        df = pd.DataFrame(rows)
        return df
    except OperationalError as e:
        print("An operational error occurred:", e)
    except Error as e:
        print("A database error occurred:", e)
    finally:
        cur.close()
        conn.close()



if __name__ == "__main__":
    df=get_movie_data()
    df.to_csv('sample.movies')

