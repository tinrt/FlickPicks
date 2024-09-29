import pandas as pd
import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
    host="localhost",
    dbname="moviedata",
    user="postgres",
    password="1234",
    port=5432
)
cur = conn.cursor()

Movie_data = 'movies_metadata.csv'  
df = pd.read_csv(Movie_data)

df['adult'] = df['adult'].astype(bool)
df['video'] = df['video'].astype(bool)

insert_query = sql.SQL('''
        INSERT INTO movies (
            adult, belongs_to_collection, budget, genres, homepage, id, imdb_id,
            original_language, original_title, overview, popularity, poster_path,
            production_companies, production_countries, release_date, revenue,
            runtime, spoken_languages, status, tagline, title, video, vote_average,
            vote_count
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) ON CONFLICT (imdb_id) DO NOTHING;
    ''')

for index, row in df.iterrows():
        cur.execute(insert_query, (
            row['adult'],
            row['belongs_to_collection'],
            row['budget'],
            row['genres'],
            row['homepage'],
            row['id'],
            row['imdb_id'],
            row['original_language'],
            row['original_title'],
            row['overview'],
            row['popularity'],
            row['poster_path'],
            row['production_companies'],
            row['production_countries'],
            row['release_date'],
            row['revenue'],
            row['runtime'],
            row['spoken_languages'],
            row['status'],
            row['tagline'],
            row['title'],
            row['video'],
            row['vote_average'],
            row['vote_count']
        ))

conn.commit()

if cur:
    cur.close()
if conn:
    conn.close()