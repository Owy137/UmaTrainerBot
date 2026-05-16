# UmaTrainerBot
Simple automated bot to train legacies for Umamusume using keyboard to prevent cursor bot detection

## Work in progress!
Current is only able to read information from displays, cannot perform actions yet!

# Setup
1. Download the files from the repository into a directory of your choosing
2. In a cmd terminal (using VSCode as example), navigate into the folder contents were downloaded into
3. Input cmd "python -m venv .venv" to create a virtual environment
    - Name of ".venv" is not required, but used as it is the default venv name in VSCode
4. Enter the cmd ".venv/Scripts/activate" to activate the virtual environment
    - If using VSCode, the name of your virtual environment should appear in green before the working tree in the terminal
5. Enter "pip install -r requirements.txt" to install required libraries
6. To run program, enter "python main.py" into cmd
    - The game should be opened into the main page of a career (where trainers can select actions to take)