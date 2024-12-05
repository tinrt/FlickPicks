# FlickPicks: Reviews, Stats, Recommendations

## Overview
FlickPicks is an interactive movie selection dashboard that offers:
- General information about a selected movie.
- Summarized reviews from IMDB.
- Top three similar film recommendations based on:
  - Similar users' tastes (user-based recommendation).
  - The movie's attributes (content-based recommendation).

## Table of Contents
1. [Goals](#goals)
2. [Frameworks and Tools](#frameworks-and-tools)
3. [Limitations](#limitations)
4. [Data Flows and Diagrams](#data-flows-and-diagrams)
5. [Software Documentation](#software-documentation)
6. [Database Documentation](#database-documentation)

---

## Goals
- Provide a user-friendly movie selection platform.
- Gather and maintain a useful database of movie reviews.
- Compare user-based and content-based recommendation systems.
- Showcase the abilities of language models in daily tasks.

---

## Frameworks and Tools
- **Data Collection:** `BeautifulSoup`, `Scrapy`, `Selenium`
- **Database Setup:** `PostgreSQL`
- **Recommendation System:** `PyTorch`, `TensorFlow`
- **Review Summarization:** `T5`, `FineBERT`
- **Interactive Dashboard:** `Flask`, `HTML`, `CSS`

---

## Limitations
1. The movie database is restricted to 22,893 titles, limiting recommendations to this set.
2. Performance is impacted due to the use of language models and recommendation models on a local machine with limited processing power, resulting in slower execution.

---

## Software Documentation

### 1. Software Interface
- **HTML Resources:** Located in the `Template` folder.
  - **`home.html`:** Main page with a movie search box.
  - **`error.html`:** Error handling page for 404 or input-related errors.

### 2. Project Modules
| Module               | Description                                                                                 |
|----------------------|---------------------------------------------------------------------------------------------|
| `header.py`          | Includes all required packages as a header file.                                           |
| `DatabaseConfig.py`  | Creates initial database tables (`movies`, `ratings`, `reviews`).                          |
| `IMDBCrawler_temp.py`| Crawls movie reviews from IMDB and saves them in the `reviews` table.                       |
| `LoadMovieData.py`   | Loads movie data into the `movies` table from `movies_metadata.csv`.                        |
| `LoadRatingData.py`  | Loads rating data into the `ratings` table from `ratings.csv`.                              |
| `Content_req.py`     | Develops the content-based recommendation model.                                            |
| `Content_req_test.py`| Provides a use case for the content-based recommendation model.                             |
| `User_req.py`        | Develops the user-based recommendation model.                                               |
| `MovieData.py`       | Prepares general movie information.                                                        |
| `Review_Summary.py`  | Summarizes IMDB reviews for a selected movie.                                               |
| `Pipeline.py`        | Main pipeline demonstrating functionality: review summaries, recommendations, and details.  |
| `app.py`             | Implements the Flask application for the dashboard.                                         |


---

Feel free to fork this repository, submit issues, or contribute enhancements. Happy movie exploration! 🎥
