import requests
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
import random
from psycopg2 import Error

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows; Windows NT 10.2; Win64; x64; en-US) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/50.0.2945.140 Safari/600.4 Edge/9.65857",
    "Mozilla/5.0 (Linux i654 x86_64; en-US) Gecko/20100101 Firefox/66.3",
    "Mozilla/5.0 (Windows; Windows NT 10.5; WOW64) AppleWebKit/533.12 (KHTML, like Gecko) Chrome/49.0.1035.350 Safari/600.6 Edge/11.33481",
    "Mozilla/5.0 (Linux; U; Linux i553 x86_64; en-US) Gecko/20130401 Firefox/67.7",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 7_8_3; en-US) AppleWebKit/602.31 (KHTML, like Gecko) Chrome/54.0.1227.181 Safari/600",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_3; like Mac OS X) AppleWebKit/603.45 (KHTML, like Gecko) Chrome/50.0.2138.229 Mobile Safari/533.2",
    "Mozilla/5.0 (compatible; MSIE 11.0; Windows; U; Windows NT 6.2;; en-US Trident/7.0)",
    "Mozilla/5.0 (Windows NT 10.2; Win64; x64) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/49.0.2187.339 Safari/600.8 Edge/11.98308",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_9; like Mac OS X) AppleWebKit/535.10 (KHTML, like Gecko) Chrome/48.0.2178.202 Mobile Safari/601.2",
    "Mozilla/5.0 (Linux; U; Linux x86_64) AppleWebKit/535.15 (KHTML, like Gecko) Chrome/48.0.1025.180 Safari/602"
]


def get_movie_reviews(movie_id):
    url = f"https://www.imdb.com/title/{movie_id}/reviews/?ref_=tt_urv"
    headers = {
        'User-Agent': random.choice(user_agents)  
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.content, 'html.parser')
    reviews = soup.select('div.text.show-more__control, div.text.show-more__control.clickable')
    review_texts = [review.get_text(strip=True) for review in reviews]
    return review_texts



def scrape_multiple_movies(movie_ids, cur, conn):
    for movie_id in movie_ids:
        reviews = get_movie_reviews(movie_id)

        for review in reviews:
            try:
                cur.execute(
                    """
                    INSERT INTO reviews (imdb_id, review)
                    VALUES (%s, %s)
                    """,
                    (movie_id, review)
                )
            except Exception as e:
                continue  

    conn.commit()

try:
    conn = psycopg2.connect(
        host="localhost",
        dbname="moviedata",
        user="postgres",
        password="1234",
        port=5432
    )
    cur = conn.cursor()
    
    cur.execute("SELECT imdb_id FROM movies;")
    rows = cur.fetchall()

    movie_ids = [row[0] for row in rows]

    scrape_multiple_movies(movie_ids, cur, conn)

except Error as db_error:
    print(f"Database connection error: {db_error}")

finally:
    if cur:
        cur.close()
    if conn:
        conn.close()