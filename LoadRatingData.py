import psycopg2
import csv
from psycopg2.extras import execute_values

conn = psycopg2.connect(
    host="localhost",
    dbname="moviedata",
    user="postgres",
    password="1234",
    port=5432
)

cur = conn.cursor()

with open('ratings.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = []
    for row in reader:
        userId = int(row['userid'])
        movie_id = row['movieid']
        rating = float(row['rating'])
        timestamp = int(row['timestamp'])
        data.append((userId, movie_id, rating, timestamp))

execute_values(cur, """
    INSERT INTO ratings (userId, movie_id, rating, timestamp)
    VALUES %s
""", data)

conn.commit()
cur.close()
conn.close()
