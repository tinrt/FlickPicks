# Movie Recommendation System (Final Project)

Author: Tina Nosrati  
Branch: cmps530  

A simple Flask-based movie recommender using user ratings.  
Recommends movies by finding users with similar preferences and suggesting movies they liked.

## How it works
- User enters/selects User ID
- Finds movies rated >=4 by the user
- Locates other users who also liked those movies
- Suggests movies those users rated highly
- Displays: Title, Genres, Overview, Rating (1-5), Release Date

## Files
Final/
- app.py          → Flask server
- model.py        → Recommender logic
- header.py       → Imports/utilities
- data/           → CSV files (movies + ratings)
- templates/      → index.html (frontend)
- static/         → style.css (styling)

## Run
cd Final  
python app.py  
open browser → http://127.0.0.1:5000/

## Requirements
Python, Flask, Pandas  
movies_metadata.csv + ratings.csv

## Features
- Clean genre formatting
- Rating shown as number only
- Simple recommendation logic
- Web interface

