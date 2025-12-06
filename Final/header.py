'''
Author: Tina Nosrati
Last Update: 12/6/2025

'''

import pandas as pd
import random
from psycopg2 import OperationalError, Error
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
import ast
import os
import torch
from flask import Flask, render_template, request
import csv
import datetime