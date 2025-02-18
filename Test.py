from movieAPI import movie_api
from movieData import get_movie_data, get_movie_id
from scrapeMovieQuotes import scrape_quote
from flask import Flask, request, jsonify
from movieData import get_movie_data, get_movie_id
from scrapeMovieQuotes import scrape_quote
from dotenv import load_dotenv
import os
import requests
from fuzzywuzzy import fuzz 

import sys
sys.stdout.reconfigure(line_buffering=True)  # Ensures print statements appear immediately




load_dotenv()

# API Keys
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
DEEPL_API = os.getenv("DEEPL_API")
DEEPL_URL = os.getenv("DEEPL_URL")
VALID_API_KEYS = [key.strip() for key in os.getenv("API_KEYS", "").split(",")]  

movie_data = movie_api('Inception', BASE_URL, API_KEY)
print(movie_data)