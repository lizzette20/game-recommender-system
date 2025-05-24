import requests 

# generates a personalized game review using Ollama based on title, genre, and mood
def generate_game_review(title, genre, mood):
    # builds the custom prompt we’ll send to Ollama
    prompt = f"""
    You're a video game expert who writes concise but fun reviews.
    Review this game for someone who is currently in the mood: {mood}.
    Game Title: {title}
    Genre(s): {genre}
    Provide a 4-5 sentence review that fits the mood.
    """

#checks if Ollama is running and API is reachable
    try:
        #sending the request to Ollama’s local API
        response = requests.post(
            "http://localhost:11434/api/generate",  #default Ollama endpoint
            json={
                "model": "tinyllama",    #model name we're using
                "prompt": prompt,        #the custom prompt we made
                "stream": False,         #no streaming needed for short reviews
                "temperature": 0.7       #controls randomness; balanced creativity for tone/variation
            },
            timeout=30  #if it takes more than 30 sec, cancel it
        )

        #checks if the request to Ollama was successful
        if response.status_code == 200:
            result = response.json()  #converts the JSON response to a Python dictionary
            return result.get("response", "No review returned.") #returns the generated text or fallsback
        else:
            return f"Error: Ollama returned status code {response.status_code}"

    except Exception as e:
        #catches any other errors (ex: if Ollama isn’t open)
        return f"Error: {str(e)} – is Ollama running?"
