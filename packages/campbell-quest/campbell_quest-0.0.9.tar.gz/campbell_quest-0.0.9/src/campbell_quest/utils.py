def load_json(filename):
    try:
        with open(f"{filename}.json", "r") as file:
            info = file.read()
            return info
    except FileNotFoundError:
        print("The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
quest_schema = load_json("quest_schema")

def get_quest_schema():
    return quest_schema