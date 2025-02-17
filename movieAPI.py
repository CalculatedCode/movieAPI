from flask import Flask, request, jsonify
from movieData import get_movie_id, get_movie_data
from scrapeMovieQuotes import scrape_quote
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

# API Keys
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
DEEPL_API = os.getenv("DEEPL_API")
DEEPL_URL = os.getenv("DEEPL_URL")
VALID_API_KEYS = [key.strip() for key in os.getenv("API_KEYS", "").split(",")] # Convert API keys to a list

# Initialize Flask app
app = Flask(__name__)

def authenticate_request():
    """Check if the request contains a valid API key."""
    api_key = request.headers.get("X-API-KEY")  
    if not api_key or api_key not in VALID_API_KEYS:
        return jsonify({"error": "Unauthorized. Invalid API key."}), 403
    return None  # No error means authentication passed

def translate_quote(quote, target_lang):
    """Translate a movie quote using DeepL API."""
    headers = {"Authorization": f"DeepL-Auth-Key {DEEPL_API}"}
    params = {
        "text": quote,
        "target_lang": target_lang.upper(),
    }

    response = requests.post(DEEPL_URL, data=params, headers=headers)
    return response.json()["translations"][0]["text"] if response.status_code == 200 else None

def movie_api(movie_title, target_lang=None):
    """Fetch movie details, a quote, and optionally translate the quote."""
    try:
        movie_id, title, year = get_movie_id(movie_title, API_KEY, BASE_URL)
        movie_data = get_movie_data(movie_id, API_KEY, BASE_URL)

        title = movie_data.get('title', 'Unknown Title')
        overview = movie_data.get('overview', 'No description available.')
        poster_url = movie_data.get('poster_url', 'No poster available.')

        quote = scrape_quote(title)
        translated_quote = translate_quote(quote, target_lang) if target_lang else None

        return {
            "title": title,
            "description": overview,
            "poster_url": poster_url,
            "quote": quote,
            "translated_quote": translated_quote
        }
    except Exception as e:
        return {"error": str(e)}

@app.route("/get_movie", methods=["POST"])
def get_movie():
    """API endpoint to fetch movie data and optionally translate a quote."""
    auth_error = authenticate_request()
    if auth_error:
        return auth_error  # Return 403 if authentication fails

    data = request.json
    movie_title = data.get("title")
    target_lang = data.get("target_lang") 

    if not movie_title:
        return jsonify({"error": "Movie title is required"}), 400

    result = movie_api(movie_title, target_lang)
    return jsonify(result)

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
