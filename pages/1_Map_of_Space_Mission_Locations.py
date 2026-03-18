import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(
    page_title="Map of Space Mission Locations"
)

if "filtered_df" in st.session_state:
    df = st.session_state["filtered_df"]
    st.pydeck_chart(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "ColumnLayer",
                data=df,
                get_position=["lng", "lat"],
                get_elevation="count",
                elevation_scale=100
            )
        ]
    )
else:
    st.write("No missions have been selected. Please make sure your filters allow for missions at the home page table.")