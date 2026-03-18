import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(
    page_title="Map of Space Mission Locations"
)

st.write("""This map shows the locations of space missions according to the filtered table on the home page. \
             The taller and whiter the column means more missions took place at that location. \
             Note that the height of the columns are relative to the max mission count of all the locations in the filtered table.
        """)

if "filtered_df" in st.session_state:

    df = st.session_state["filtered_df"]
    groupedDF = df.groupby(["Longitude", "Latitude", "Location"])["Mission"].count()

    sortedDF = groupedDF.reset_index(name="Count")
    maxCount = sortedDF["Count"].max()

    st.pydeck_chart(
        pdk.Deck(
            map_style=None,  # Use Streamlit theme to pick map style
            initial_view_state=pdk.ViewState(
                latitude=sortedDF["Latitude"].iloc[0],
                longitude=sortedDF["Longitude"].iloc[0],
                zoom=1,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    "ColumnLayer",
                    data=sortedDF,
                    get_position=["Longitude", "Latitude"],
                    get_elevation="Count",
                    elevation_scale=2000000/maxCount,
                    radius=50000,
                    auto_highlight=True,
                    pickable=True,
                    elevation_range=[0, 2000000],
                    extruded=True,
                    get_fill_color=f'[255, 255, (Count/{maxCount}) * 255]'
                )
            ]
        )
    )
else:
    st.write("No missions have been selected. Please make sure your filters allow for missions at the home page table.")
