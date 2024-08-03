import ollama

def format_quest(quest, reward, schema):
    formatter_system_prompt = (f"You are a helpful AI Assistant at a game studio.\n"
    f"Your task is to encode a given quest into a JSON format according to the provided schema.\n"
    f"Review the quest and generate a JSON output that strictly adheres to the schema.\n"
    f"Ensure the output is valid JSON without including any additional text.\n"
    f"The output should ONLY include the valid JSON.\n"

    f"\n###\n"
    
    f"Quest:"
    f"{quest}\n"
    
    f"\n###\n"
    
    f"Reward:"
    f"{reward}\n"
    
    f"\n###\n"

    f"Schema:"
    f"{schema}\n")
    
    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": formatter_system_prompt
        }
    ], options={"temperature": 0.1})

    return response["message"]["content"]