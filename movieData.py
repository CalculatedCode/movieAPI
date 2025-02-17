import requests

import requests

def get_movie_id(movie_title, API_KEY, BASE_URL):
    """Find the best matching movie title (case-insensitive, prefers exact matches)."""
    search_url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": movie_title}
    
    response = requests.get(search_url, params=params)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return None

    results = response.json().get("results", [])

    if not results:
        print("No movies found for the given title.")
        return None

    # Normalize input title
    lower_title = movie_title.lower()
    best_match = None

    # Check all results for an exact match (case-insensitive)
    for movie in results:
        if movie["title"].lower() == lower_title:
            best_match = movie  # Found an exact match, break early
            break

    # If no exact match, use the first result from the API
    if not best_match:
        best_match = results[0]

    return best_match["id"], best_match["title"], best_match.get("release_date", "Unknown Release Date")

    

    

def get_movie_data(movie_id, API_KEY, BASE_URL):
    movie_url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    response = requests.get(movie_url, params=params)

    if response.status_code == 200:
        data = response.json()
        title = data.get("title", "Unknown Title")
        overview = data.get("overview", "No description available.")
        poster_path = data.get("poster_path")

        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            poster_url = "No poster available."

        return {"title": title, "overview": overview, "poster_url": poster_url}

    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

