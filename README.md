# Quick Reference for Space Mission Dashboard Project

## Setup

```bash
# Install required packages
pip3 install -r requirements.txt

# Run streamlit to create dashboard in web browser locally
streamlit run Space_Missions_Table_Home.py

# If the above does not work, try this command
python3 -m streamlit run Space_Missions_Table_Home.py
```

Note that the three visualizations are dependent on the filters in the home page. Thus, using a filter on the home table also modifies the visualizations.

## Project Structure
```
📦 
├─ README.md
├─ Space_Missions_Table_Home.py               # Entry point for Streamlit dashboard
├─ get_coor.py                                # Helper script to get coordinates for the locations in the missions CSV
├─ pages                                      # Contains the pages for each of the three visualizations
│  ├─ 1_Map_of_Space_Mission_Locations.py
│  ├─ 2_Success_Rate_over_Time.py
│  └─ 3_Missions_by_Company.py
├─ required_functions.py                      # The eight required functions
├─ requirements.txt
├─ space_missions.csv
└─ space_missions_with_coor.csv               # space_missions.csv with the coordinates of each location appended as lat/long columns
```

## Why I chose Streamlit for each visualization

Streamlit has an easy-to-use interface with support for a variety of Python visualization packages such as PyDeck and Vega-Altair.

It made it possible to overlay a world map, a bar chart, and a line chart all within the same web interface.

The three visualizations were chosen based on how different each of them were. I didn't want to do three line charts but instead a diversity of visualizations, all possible thanks to Streamlit and acccompanying packages.
