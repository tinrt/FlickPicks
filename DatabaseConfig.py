import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="moviedata",
    user="postgres",
    password="1234",
    port=5432
)
cur = conn.cursor()

try:
    # Create movies table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        adult BOOLEAN,
        belongs_to_collection TEXT,
        budget BIGINT,
        genres TEXT,
        homepage TEXT,
        id TEXT PRIMARY KEY,
        imdb_id TEXT UNIQUE,
        original_language TEXT,
        original_title TEXT,
        overview TEXT,
        popularity DOUBLE PRECISION,
        poster_path TEXT,
        production_companies TEXT,
        production_countries TEXT,
        release_date TEXT,
        revenue BIGINT,
        runtime INTEGER,
        spoken_languages TEXT,
        status TEXT,
        tagline TEXT,
        title TEXT,
        video BOOLEAN,
        vote_average DOUBLE PRECISION,
        vote_count INTEGER
    )
    """)

    # Create ratings table with foreign key to movies (id column)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ratings (
        userId INT,
        movie_id TEXT,
        rating DOUBLE PRECISION,
        timestamp BIGINT,
        FOREIGN KEY (movie_id) REFERENCES movies(id)
    )
    """)

    # Create reviews table with foreign key to movies (imdb_id column)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        imdb_id TEXT,
        review TEXT,
        FOREIGN KEY (imdb_id) REFERENCES movies(imdb_id)
    )
    """)
    
    conn.commit()
    
except Exception as e:
    print("An error occurred:", e)
finally:
    cur.close()
    conn.close()
