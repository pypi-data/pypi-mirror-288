from .questAgents import quest_brainstormer, quest_refiner, quest_formatter

def generate_quest(quest_prompt, schema, objective_info, location_info, character_info, rewards):
    
    initial_generated_quest = quest_brainstormer.generate_quest(objective_info, quest_prompt, location_info, character_info)
    
    quest_with_objectives = quest_refiner.define_quest_objectives(initial_generated_quest, location_info, character_info)
    
    quest_reward = quest_refiner.define_quest_reward(initial_generated_quest, rewards)
    
    formatted_quest = quest_formatter.format_quest(quest_with_objectives, quest_reward, schema)
    
    return formatted_quest
    