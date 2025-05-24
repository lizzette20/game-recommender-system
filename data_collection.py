import requests 
import json
import pandas as pd
import os 
from dotenv import load_dotenv
import sqlite3

"""
This script collects video game data from the RAWG Video Games Database API. It fetches game metadata such as names, genres, and ratings, and stores the results in a local SQLite database ('games.db'). 
The API key is loaded securely from a '.env' file. 
This script supports up to 40 games per request and structures the data using pandas for further analysis or use in recommendation systems.

Usage:
    1. Create a .env file containing your RAWG_API_KEY.
    2. Install dependencies: pip install -r requirements.txt
    3. Run the script: python data_collection.py
"""



#Loading environment variables from .env file
load_dotenv()
api_key = os.getenv('RAWG_API_KEY')

#Setting the API endpoint
api_url = "https://api.rawg.io/api/games"

#Setting the parameters for the API request
#The parameters include the API key, page number, and page size
params = {
    "key": api_key,
    "page": 1, 
    "page_size": 40  #Number of results per page
    }

#Making a request to the API with the parameters
r=requests.get(api_url, params=params)

#Mood-to-genre mapping to support mood-based recommendations
mood_map = {
    "excited": ["Racing", "Massively Multiplayer", "Sports"],
    "happy": ["Indie", "Platformer"],
    "curious": ["Puzzle", "Adventure"],
    "suspenseful": ["Shooter"],
    "immersive": ["RPG"],
    "intense": ["Action"]
}

#Checking the request was successful
if r.status_code == 200:
    print("Request was successful")

    #Extracting the data from the response if successful
    data=r.json()

    #Formatting the data for better readability
    formatted_json=json.dumps(data, sort_keys=True, indent=5)
    #print(formatted_json)

    #Extracting the list of game results safely
    results = data.get('results', [])

    #Initializing an empty list to store game details
    all_games = []

    for game in results:
        #Extracting game names and ratings safely, using 'N/A' if the key is missing
        game_name = game.get('name', 'N/A')
        game_rating = game.get('rating', 'N/A')
        
        #Initializing an empty list to collect genre names
        genre_names = []

        #Loops through each genre dictionary and extracts the 'name' field
        for genre in game.get('genres', []):
            #Appends the genre name to the genre_names list
            #Using 'N/A' if the genre name is missing
            genre_names.append(genre.get('name', 'N/A'))

        #Converts the list of genre names into a string seperated by commas
        game_genres = ", ".join(genre_names)

        #Default mood if none matched
        game_mood = "unknown"
        #Checks if any of the genres match the mood_map
        #If a match is found, assigns the corresponding mood to game_mood
        for mood, genres in mood_map.items():
            if any(genre in genres for genre in genre_names):
                game_mood = mood
                break

        #Prints a formatted summary of the game's name, genres, and rating
        print(f'Game Name: {game_name}, Genres: {game_genres}, Rating: {game_rating}')

        #Appends the game details to the all_games list
        all_games.append({
        'name': game_name,
        'genres': game_genres,
        'rating': game_rating,
        'mood': game_mood
        })

    #Creating a DataFrame from the list of games
    df = pd.DataFrame(all_games)
    print(df.head())  #Printing first few rows
    print(df.columns) #Printing column names

    #Saving to a Sqlite database
    conn = sqlite3.connect('games.db')
    df.to_sql('games', conn, if_exists='replace', index=False)
    conn.close()
    #Printing success message
    print("Data saved to SQLite database successfully.")

    #Printing all the collected games
    print("All Collected Games: ")
    for game in all_games:
            print(game)
else:
    #If the request was not successful, print the status code and response
    print("Request failed with status code:", r.status_code)
    print("Response:", r.text)




