import os

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Extract the directory containing the script file
script_directory = os.path.dirname(script_path)

# Change the working directory 
os.chdir(f"{script_directory}\\schemas")