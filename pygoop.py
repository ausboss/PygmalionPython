import requests
import re
import json

endpoint = "https://boc-chosen-affectesdfsdfd-contamination.trycloudflare.com/"


class Character:
    def __init__(self, filename, history):
        with open(filename, "r") as f:
            data = json.load(f)
            self.name = data["char_name"]
            self.persona = data["char_persona"]
            self.greeting = data["char_greeting"]
            self.world_scenario = data["world_scenario"]
            self.example_dialogue = data["example_dialogue"]
            self.update_history(history)

    def update_history(self, history):
        # Define the conversation history for this character
        conversation_history = f"{self.name}'s Persona: {self.persona}\n" + \
                               f"World Scenario: {self.world_scenario}\n" + \
                               f'<START>\n' + \
                               f'{self.example_dialogue}' + \
                               f'<START>\n' + \
                               f"{self.name}: {self.greeting}\n"
        # Reset the history attribute of the History object
        history.history = [conversation_history[1:]] # Remove the initial '\n' character



class History:
    def __init__(self):
        self.history = []
        self.prompt = None

    def generate_response(self, endpoint):
        # Generate response based on the user's message and the prompt
        response = requests.post(f"{endpoint}/api/v1/generate", json=self.prompt)
        results = response.json()['results']
        # extract the correct bot reponse from the large json of information
        text = results[0]['text']
        parts = re.split(r'\n[a-zA-Z]', text)
        response_text = parts[0]
        # add the response to history
        if len(self.history) > 100:
            self.history = self.history[-100:]
        return response_text

    def add_message(self, speaker, message):
        self.history.append(f"{speaker}: {message}\n")

    def save_conversation(self, character, user_input):
        self.add_message("You", user_input)
        self.prompt = {"prompt": '\n'.join(self.history[-10:]) + f"{character.name}:", "use_story": False, "use_memory": False, 
                    "use_authors_note": False, "use_world_info": False, "max_context_length": 1818, 
                    "max_length": 120, "rep_pen": 1.03, "rep_pen_range": 1024, "rep_pen_slope": 0.9, 
                    "temperature": 0.98, "tfs": 0.9, "top_a": 0, "top_k": 0, "top_p": 0.9, 
                    "typical": 1, "sampler_order": [6, 0, 1, 2, 3, 4, 5]}
        bot_response = self.generate_response(endpoint)
        self.add_message(character.name, bot_response)
        return bot_response
    
history = History()
character = Character("rise.json", history)

print(f"{character.name}: {character.greeting}")

# Start the game loop
while True:
    # Prompt the user for input
    user_input = input("You: ")

    # Save the user input and generate a bot response
    bot_response = history.save_conversation(character, user_input)

    # Print the chat bot's response
    print(f"{character.name}: " + bot_response)

    # If the chat bot responds with a terminating message, exit the loop
    if bot_response in ['Goodbye.', 'See you later.']:
        break
