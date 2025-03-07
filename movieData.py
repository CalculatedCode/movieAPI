import requests
from fuzzywuzzy import fuzz

def get_movie_id(movie_title, BASE_URL, API_KEY, release_year=None):
    """Find the best matching movie id by fuzzy matching title and optional release year."""

    #make request to "The Movie Database"
    search_url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": movie_title}
    response = requests.get(search_url, params=params)
    
    #validate response code
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return None

    #get and validate results
    results = response.json().get("results", [])
    if not results:
        print("No movies found for the given title.")
        return None

    #convert title to lower case and initialize variables for fuzzy matching
    lower_title = movie_title.lower()
    best_match = None
    highest_score = 0

    #preform our fuzzy match
    for movie in results:
        movie_title_lower = movie["title"].lower()
        score = fuzz.ratio(lower_title, movie_title_lower)  # Compute similarity score

        # If a release year is provided, boost matches with correct year
        movie_year = movie.get("release_date", "")[:4] 
        if release_year and movie_year == str(release_year):
            score += 15  

        # Select the highest-scoring title
        if score > highest_score:
            highest_score = score
            best_match = movie

    #Duplicate error checking (as long as the list isn't empty A movie should be returned)
    if not best_match:
        print("No suitable match found.")
        return None

    return best_match["id"], best_match["title"], best_match.get("release_date", "Unknown Release Date")

    

    

def get_movie_data(movie_id, BASE_URL, API_KEY):
    """Return the movie data (title, overview and poster path) from The Movie Database
    using movie ID"""

    #Make request to The Movie Database
    movie_url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }
    response = requests.get(movie_url, params=params)

    #validate data and get response values
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

