import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(
    page_title="Success Rate over Time"
)

st.write("""This graph shows the succcess rate of space missions per year according to the filtered table on the home page. 
        """)

def success_sum(group):
    return group[group["MissionStatus"] == "Success"]["Count"].sum()

def overall_sum(group):
    return group["Count"].sum()

if "filtered_df" in st.session_state:

    df = st.session_state["filtered_df"]
    df["Year"] = pd.to_datetime(df["Date"]).dt.year
    groupedDF = df.groupby(["Year", "MissionStatus"])["Mission"].nunique()
    groupedDF = groupedDF.reset_index(name="Count")
    
    successDF = groupedDF.groupby("Year").apply(success_sum)

    overallDF = groupedDF.groupby("Year").apply(overall_sum)

    rate = (successDF/overallDF).to_frame()
    rate.index = rate.index.astype(str)
    rate.rename(columns={0: "Success Rate"}, inplace=True)
    
    st.line_chart(rate, x_label="Year", y_label="Success Rate")
    


else:
    st.write("No missions have been selected. Please make sure your filters allow for missions at the home page table.")
