import ollama

def generate_quest(objective_info, quest_prompt, locations, characters):
    brainstorming_system_prompt = (f"You are a Quest Designer at a Game studio.\n"
    f"You have been tasked with creating compelling Side-Quests for a Role-Playing Game.\n"
    f"The game is set in a Fantasy setting.\n"
    f"Consider the locations and characters given and generate a quest.\n"

    f"\n###\n"

    f"The quest should be of a type outlined in the \"quest_objectives\" below:\n"

    f"{objective_info}\n"
    
    f"\n###\n"

    f"\n###\n"

    f"Locations:\n"
    f"{locations}\n"
    
    f"\n###\n"
    
    f"Characters:\n"
    f"{characters}\n")
    
    brainstorming_user_prompt = (f"As a Quest Designer at a Game Studio, your task is to generate an appropriate quest based on the given quest prompt and system instructions.\n"
    f"Ensure you do not introduce new characters or locations, and avoid adding any extra requirements or restrictions.\n"
    f"Use only the provided characters and locations that fit logically within the context of the quest.\n"
    f"Avoid adding any new information to the existing locations.\n"
        
    f"\n###\n"
    
    f"Quest Prompt:\n"
    f"{quest_prompt}\n"

    f"\n###\n"

    f"\nDescribe the quest in the format given:\n"
    f"Name:\nType:\nGoal:\nDescription:\n"

    f"\n###\n"

    f"Remember to adhere to the system instructions.\n")

    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": brainstorming_system_prompt
        },
        {
            "role": "user",
            "content": brainstorming_user_prompt
        }
    ], options={"temperature": 1.2})

    return response["message"]["content"]