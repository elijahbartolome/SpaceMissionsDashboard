import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from streamlit_dynamic_filters import DynamicFilters

st.set_page_config(
    page_title="Space Missions Table Home"
)
# Columns for reference: 
# Company,Location,Date,Time,Rocket,Mission,RocketStatus,Price,MissionStatus
df = pd.read_csv("space_missions_with_coor.csv")
df["Date"] = pd.to_datetime(df["Date"]).dt.date

# Filters
dynamic_filters = DynamicFilters(df, filters=["Company", "Location", "Rocket", "Mission", "RocketStatus", "MissionStatus"])
dynamic_filters.display_filters(location="sidebar")
filtered_df = dynamic_filters.filter_df()

# Date Filters
default_start_date = dt.date(1957, 10, 4) #Earliest mission
default_end_date = dt.date.today()
try:
    start_date, end_date = st.sidebar.date_input("Select a date range", value=(default_start_date, default_end_date))
    mask = (filtered_df["Date"] >= start_date) & (filtered_df["Date"] <= end_date)
    filtered_df = filtered_df.loc[mask]
except:
    pass

# Save filtered dataframe for visualizations on other pages
st.session_state["filtered_df"] = filtered_df

# Display Table
st.write("Space Missions")
st.dataframe(filtered_df)

# Display Summary Statistics (adjusts based on filters)
st.write("Summary Statistics")
summary_stats = filtered_df.describe(include=object).rename(index={"count":"Count", "unique":"Number of Unique Values", "top":"Most Common", "freq":"Most Common Value's Frequency"})
st.dataframe(summary_stats, use_container_width=True) 

# Success Rate
st.write("Success Rate")
numMissions = len(filtered_df["Mission"].unique())
if numMissions == 0:
    st.write(0.0)
else:
    numSuccess = len(filtered_df[filtered_df["MissionStatus"] == "Success"]["Mission"].unique())
    st.write(round((numSuccess/numMissions) * 100, 2))