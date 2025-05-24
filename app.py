import gradio as gr
import random
import sqlite3
from generate_review import generate_game_review

print (gr.__version__) #prints the installed gradio version to verify enviroment

# Game recommendation fucntion using mood + genre from SQLite
def recommend_game(mood,gaming_style=None):
    # Connecting to the database file
    connection = sqlite3.connect("games.db")
    cursor = connection.cursor()

    # Formatting inputs
    mood = mood.lower()
    genre = gaming_style.lower()

#SQL query: trying to fetch games that match both mood and genres
if genre != "any":
    cursor.execute("""
                   SELECT name, rating, genres, mood
                   FROM games
                   WHERE LOWER(mood) = ? AND LOWER(genres) LIKE?""",(mood,f"%{genre}%"""))
else:
    cursor.execute("""
                   SELECT name, rating, genres, mood
                   FROM games
                   WHERE LOWER (mood) = ?""",(mood,))

#Fetching result from the database
results = cursor.fetchall()
connection.close()

# If no games are found, return an appropriate fallback message
if not results:
    return f"Sorry, I don't have recommendations for that mood. Try: immersive, intense, suspenseful, or curious"
# Randomly select up to 2 games
selected_games = random.sample(results,min(2,len(results))) 

# Formatting the recommendations for display
recommendations = f" ## Game Recommendations for {mood.capitalize()} Mood \n\n"
for game in selected_games:
    name, rating, genres, mood_value = game
    recommendations += f" ## {name} — {rating}\n"
    recommendations += f"**Genres:**{genres}\n"
    recommendations += f"**Mood:**{mood_value}\n"

#Adding the AI-generated review using our Ollama function
review = generate_game_review(name, genres, mood)
recommendations +=f"**AI Review:**{review}\n\n"

return recommendations

# Creating the interface
demo = gr.Interface(
    fn = recommend_game, #the function running when users submit inputs 
    inputs= [
    #First input: users current mood
    gr.Textbox(label = "How are yoy feeling today?", placeholder ="e.g., immersive, happy, curious"),
    #Second input: users preferred gaming style
    gr.Dropdown(["Action","Shooter","RPG","Puzzle","Adventure","Strategy","Any"],
                label="Game Style (Optional)", value= "Any")
    ],
outputs=gr.Markdown(label = "Your Personalized Game Recommendations"),
title="Mood-Based Game Recommender",
description = "Get personalized game suggestions based on your current mood abd prefferd gaming style!"
)

# Launching the app with a public share link
if __name__ =="__main__":
    demo.launch(share=True) 