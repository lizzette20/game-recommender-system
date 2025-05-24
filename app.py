import gradio as gr
import random


print (gr.__version__) #prints the installed gradio version to verify enviroment

# Game recommendation fucntion using mood + genre from SQLite
def recommend_game(mood,gmaing_style=None):
    # Connecting to the database file
    connect = sqlite3.connect("games.db")
    cursor = connection.cursor()

# Formatting inputs
mood = mood.lower()
genre = genre.lower()
