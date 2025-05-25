import gradio as gr
import random
import sqlite3
from generate_review import generate_game_review

"""
This script launches a Gradio web application that recommends video games based on the user's mood and preferred genre. 

It connects to a local SQLite database ('games.db') to retrieve relevant games and uses a local Ollama language model to generate a short AI-powered game review for each suggestion.

Features:
- Takes user input for mood and optional game genre
- Recommends up to two matching games from the database
- Uses Ollama via HTTP API to generate concise, mood-aligned reviews
- Displays results through an interactive Gradio interface

Usage:
    1. Ensure 'games.db' exists and contains game data including mood and genre.
    2. Start Ollama locally with the correct model (e.g., `tinyllama`).
    3. Run this script: python app.py
    4. A public Gradio link will be generated to access the interface.
"""

print (gr.__version__) #prints the installed gradio version to verify enviroment

#Game recommendation fucntion using mood + genre from SQLite
def recommend_game(mood, gaming_style=None):
    # Connecting to the database file
    connection = sqlite3.connect("games.db")
    cursor = connection.cursor()

    #Formatting inputs
    mood = mood.lower()
    genre = gaming_style.lower()

#SQL query: trying to fetch games that match both mood and genres
    if genre != "any":
        cursor.execute("""
            SELECT name, rating, genres, mood
            FROM games
            WHERE LOWER(mood) = ? AND LOWER(genres) LIKE ?
            """, (mood, f"%{genre}%"))
    else:
        cursor.execute("""
                    SELECT name, rating, genres, mood
                    FROM games
                    WHERE LOWER (mood) = ?""",(mood,))

    #Fetching result from the database
    results = cursor.fetchall()
    connection.close()

    # If no games are found for that mood, return an appropriate fallback message
    if not results:
        return f"Sorry, I couldn't find any games matching that mood and genre.\n\n" "Try a different mood like: immersive, intense, suspenseful, or curious.\n" "Or select 'Any' under game style to broaden the results."
    # Randomly select up to 2 games
    selected_games = random.sample(results,min(2,len(results))) 

    #Formatting the recommendations for display
    recommendations = f" ## Game Recommendations for {mood.capitalize()} Mood \n\n"

    for game in selected_games:
        name, rating, genres, mood_value = game

        #Adding game information to the recommendations
        recommendations += f"### 🎮 {name} — {rating}/5\n"
        recommendations += f"- **Genres:** {genres}\n"
        recommendations += f"- **Mood:** {mood_value}\n"

        #Adding the AI-generated review using our Ollama function
        review = generate_game_review(name, genres, mood)
        recommendations += f"- **AI Review:** {review.strip()}\n\n"

    return recommendations

# Creating the interface
demo = gr.Interface(
    fn = recommend_game, #the function running when users submit inputs 
    inputs= [
    #First input: users current mood
    gr.Textbox(label = "How are yoy feeling today? 🎭", placeholder ="e.g., immersive, happy, curious"),
    #Second input: users preferred gaming style
    gr.Dropdown(["Action","Shooter","RPG","Puzzle","Adventure","Strategy","Any"],
                label="Preferred Game Style (Optional) 🎮", value= "Any")
    ],
outputs=gr.Markdown(label = "Your Personalized Game Recommendations 🎯"),
title="Mood-Based Game Recommender 🕹️",
description = "Get personalized game suggestions based on your current mood and preferred gaming style!"
)

#Launching the app with a public share link
if __name__ =="__main__":
    demo.launch(share=True) 
