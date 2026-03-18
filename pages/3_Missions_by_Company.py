import pandas as pd
import pydeck as pdk
import streamlit as st
import altair as alt

st.set_page_config(
    page_title="Missions by Company"
)

st.write("""This graph shows the number of space missions for each company according to the filtered table on the home page. 
        """)

if "filtered_df" in st.session_state:
    df = st.session_state["filtered_df"]
    groupedDF = df.groupby(["Company", "MissionStatus"])["Mission"].count()
    groupedDF = groupedDF.reset_index(name="Mission Count")

    chart = alt.Chart(groupedDF).mark_bar().encode(
        x=alt.X('MissionStatus:N', axis=None),
        y='Mission Count:Q',
        color=alt.Color('MissionStatus', 
                        scale=alt.Scale(
                            domain=['Success', 'Partial Failure', 'Prelaunch Failure', 'Failure'], 
                            range=['blue', 'yellow', 'orange', 'red']
        )),
        column='Company:N'
    )

    st.altair_chart(chart)
else:
    st.write("No missions have been selected. Please make sure your filters allow for missions at the home page table.")
