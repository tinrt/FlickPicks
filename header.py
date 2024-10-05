'''
Author: Tina Nosrati
Last Update: 10/5/2024

'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
import random
from psycopg2 import OperationalError, Error
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
import os
from transformers import pipeline