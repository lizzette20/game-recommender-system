# Game-recommender-system

This project is an AI-enhanced web application that recommends video games based on a user's current mood and preferred game genre (if any). It integrates real-time data from the RAWG Video Games Database API, stores it in a local SQLite database, and uses a local large language model (Ollama) to generate short, personalized game reviews.

## Features
- Mood and genre-based game recommendation
- AI-generated reviews using Ollama (`tinyllama`)
- Clean Gradio-powered web interface
- Locally stored SQLite database for game data

## Public Web App
You can try the deployed Gradio app here:
**[https://5e0b437c1c7617bdcc.gradio.live](https://5e0b437c1c7617bdcc.gradio.live)**  
(Note: This link will only work if the app is currently running with `share=True`.)

## Group Members
- Lizzette Rivera  
- Chelsea Tanchez
- Zhi Hao Wu Tang

## Setup Instructions

### 1. Clone the repository:
git clone https://github.com/lizzette20/game-recommender-system.git
cd game-recommender-system

## 2. Create and Activate a Virtual Environment:

```bash
python3 -m venv venv

Activate the environment:

macOS/Linux: source venv/bin/activate

Windows: venv\Scripts\activate
```
## 3. Install Dependencies
```bash
pip install -r requirements.txt
```
## 4. Adding Your API Key:
Create a .env file in the root directory.

In your .env add your RAWG API key like this:
RAWG_API_KEY=your_rawg_api_key_here

To get your API key, visit https://rawg.io/apidocs.

## 5. Run the Data Collection Script:
python data_collection.py #This script fetches game data from the RAWG API and stores it in a local SQLite database called games.db.

## 6. Start the Web Application
python app.py #Once the app launches, a local and a public URL (if share=True is set) will appear in the terminal. Open either in a browser to interact with the app.

## Requirements
Python 3.9+

Virtual environment (recommended)

Ollama (installed and running locally: https://ollama.com/)

RAWG API key

## Project Files
app.py: Gradio web app for recommendations

data_collection.py: Collects and stores game data from the RAWG API

generate_review.py: Uses Ollama to create a custom review for each game

games.db: Local database with game info

.env: File storing your private RAWG API key

requirements.txt: Python dependencies list

## Troubleshooting
gradio not found: Make sure the virtual environment is activated, then run pip install -r requirements.txt.

Ollama errors: Confirm that Ollama is installed and running (ollama run tinyllama).

Missing .env: Make sure .env exists and includes your API key.

Permission issues on Mac: Try using python3 and pip3 instead of python and pip.