import requests
import json
import os

# Set the endpoint URL
endpoint = "https://aaron-prescription-test-containers.trycloudflare.com"

characters_folder = 'Characters'
characters = []

for filename in os.listdir(characters_folder):
    if filename.endswith('.json'):
        with open(os.path.join(characters_folder, filename)) as read_file:
            character_data = json.load(read_file)
            characters.append(character_data)

for i, character in enumerate(characters):
    print(f"{i+1}. {character['char_name']}")

selected_char = int(input("Please select a character: ")) - 1

data = characters[selected_char]

# Get the character name and greeting
char_name = data["char_name"]
char_greeting = data["char_greeting"]

print("\nStarting Chat. 'q' to quit\n")
# Print the character greeting
print(char_greeting)



# Initialize the conversation history to the starting prompt
conversation_history = f"{char_name}'s Persona: {data['char_persona']}\n" + \
                       '<START>\n' + \
                       f"{char_name}: {char_greeting}"


# Define the number of lines to keep in the conversation history
num_lines_to_keep = 20

# Starts main loop that you can break with 'q'
while True:
    try:
        user_input = input("You: ")
        if user_input != "q":
            # Add the user input to the conversation history
            conversation_history += f'You: {user_input}\n'
            # Define the prompt
            prompt = {
                "prompt": '\n'.join(conversation_history.split('\n')[-num_lines_to_keep:]) + f'{char_name}:',
                "use_story": False,
                "use_memory": False,
                "use_authors_note": False,
                "use_world_info": False,
                "max_context_length": 1818,
                "max_length": 150,
                "rep_pen": 1.03,
                "rep_pen_range": 1024,
                "rep_pen_slope": 0.9,
                "temperature": 0.98,
                "tfs": 0.9,
                "top_a": 0,
                "top_k": 0,
                "top_p": 0.9,
                "typical": 1,
                "sampler_order": [
                    6, 0, 1, 2,
                    3, 4, 5
                ]
            }
            # Send a post request to the API endpoint
            response = requests.post(f"{endpoint}/api/v1/generate", json=prompt)
            # Check if the request was successful
            if response.status_code == 200:
                # Get the results from the response
                results = response.json()['results']
                # print(results)
                # Print the first result
                text = results[0]['text']
                split_text = text.split("You:")
                response_text = split_text[0].strip().replace(f"{char_name}:", "").strip()
                print(f'{char_name}: {response_text}\n')
                conversation_history = conversation_history + f'{char_name}: {response_text}\n'
            else:
                break
        else:
            print("\n\nChat Ended\n\n")
            break


    except requests.exceptions.ConnectionError:
            print("Error: there was a problem with the endpoint.")
            break
