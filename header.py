'''
Author: Tina Nosrati
Last Update: 11/8/2024

'''
import ast
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
import openai
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from flask import Flask
import csv
import datetime