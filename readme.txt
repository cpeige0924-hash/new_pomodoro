==========================================================
POMODORO PET TIMER
==========================================================

Author: Peige Cai
Project for: COMP9001 / Final Project
Main script to run: main.py

----------------------------------------------------------
1. Overview
----------------------------------------------------------
This is a Pomodoro timer application combined with a virtual pet growth system.
When users complete 25-minute or 50-minute Pomodoro sessions, their pet grows.
After reaching full growth, the pet is moved to the Garden. Focus time is also
recorded daily and can be viewed in the history section.

Main Features:
- 25-minute or 50-minute Pomodoro timer
- Pause / Resume / Quit during session
- Floating transparent timer window, always on top
- Virtual pets (cat, dog, rabbit, duck) with 3 ASCII growth stages
- Pets grow based on completed Pomodoro sessions
- Fully-grown pets are stored in the Garden
- Daily focus history display
- Data automatically saved using JSON

----------------------------------------------------------
2. How to Run
----------------------------------------------------------
1. Make sure Python 3.10 or above is installed.
2. Install the required library:
      pip install PyQt5
3. Run the main script:
      python main.py

⚠ IMPORTANT:
This is a GUI application using PyQt5. 
It CANNOT run in the EdStem environment.
Please run it locally on your own computer.

----------------------------------------------------------
3. File Structure
----------------------------------------------------------
new_pomodoro/
├── main.py                # Entry point
│
├── core/                  # Program logic & data handling
│   ├── timer.py           # Countdown timer logic
│   ├── pet.py             # Pet data model
│   ├── pet_manager.py     # Save/load pet & garden
│   ├── state_manager.py   # Daily focus tracking
│
├── ui/                    # All GUI pages
│   ├── menu_page.py       # Main menu
│   ├── pomodoro_page.py   # Timer + pet floating window
│   ├── pet_setup.py       # Create new pet dialog
│   ├── garden_page.py     # Garden pet display (if included)
│
├── (Automatically created JSON files after running:)
│   ├── petdata.json       # Current growing pet
│   ├── garden.json        # All fully grown pets
│   ├── focus_history.json # Daily focus time

----------------------------------------------------------
4. Data Storage
----------------------------------------------------------
- No manual database setup is required.
- JSON files are created automatically when the program runs.
- Deleting these files will reset pets, garden and focus records.

----------------------------------------------------------
5. Dependencies
----------------------------------------------------------
- Python 3.10+
- PyQt5

Install with:
    pip install PyQt5

----------------------------------------------------------
6. Future plans
----------------------------------------------------------
In the future, I want to make the pets feel more alive — 
not just images, but companions that react to the user’s focus, breaks and emotions. 
A feature that hasn’t been finished yet is allowing fully grown pets to continue accompanying the user. 
Later, I may limit the number of pets, 
but let each one have a stronger connection to the user’s focus history.
I also plan to add a long-term goal system and a simple mood tracking feature, 
so the app isn’t only about counting minutes, but also about understanding why we work and how we feel.

----------------------------------------------------------
End of README
----------------------------------------------------------