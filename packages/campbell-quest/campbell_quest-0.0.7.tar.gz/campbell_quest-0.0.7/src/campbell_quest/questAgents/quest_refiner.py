import ollama

def define_quest_objectives(quest, locations, characters):
    refiner_objectives_system_prompt = (f"You are a Writer at a Game studio.\n"
    f"You have been tasked with editing given Side-Quests for a Role-Playing Game.\n"
    f"The quest, the character and the location information is given to you.\n"
    f"Adhere to the information provided.\n"

    f"\n###\n"
    
    f"Quest:"
    f"{quest}\n"
    
    f"\n###\n"
    
    f"Locations:"
    f"{locations}\n"
    
    f"\n###\n"
    
    f"Characters:"
    f"{characters}\n")
    
    refiner_objectives_user_prompt = (f"As a Writer at a Game Studio, your task is to revise the quest provided in the system instructions.\n"
    f"Your goal is to rewrite the quest to include a detailed list of clear and concise objectives.\n"
    f"Each objective should outline a single, specific action that the player needs to complete.\n"
    f"Ensure that these objectives are logical and coherent within the context of the quest.\n"
    f"Use ONLY the given quest to create the objectives.\n"
    f"Do not generate any additional information beyond what is provided.\n"
    
    f"\nDescribe the quest in the format given:\n"
    f"Name:\nDescription:\nGoal:\nObjectives:\n")
    
    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": refiner_objectives_system_prompt
        },
        {
            "role": "user",
            "content": refiner_objectives_user_prompt
        }
    ], options={"temperature": 0.1})

    return response["message"]["content"]

def define_quest_reward(quest, rewards):
    refiner_rewards_system_prompt = (f"You are a Quest Designer at a Game studio.\n"
    f"You have been tasked with choosing the appropriate reward for a given Side-Quest.\n"
    f"Consider the quest provided and pick a reward from the list given.\n"
    f"ONLY pick an item from the list.\n"
    f"You MUST pick some reward.\n"

    f"\n###\n"
    
    f"Quest:"
    f"{quest}\n"
    
    f"\n###\n"
    
    f"Rewards:"
    f"{rewards}\n")
    
    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": refiner_rewards_system_prompt
        }
    ], options={"temperature": 0.1})

    return response["message"]["content"]