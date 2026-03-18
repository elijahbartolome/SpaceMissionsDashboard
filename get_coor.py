import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from geopy.extra.rate_limiter import RateLimiter
import os
from dotenv import load_dotenv, dotenv_values 
import re

load_dotenv()

geolocator = GoogleV3(api_key=os.getenv("API_KEY"), timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)

df = pd.read_csv("space_missions.csv")
print(df["Location"])
df["Location"] = df["Location"].apply(lambda x: re.sub(r'^[^,]*,\s*', '', x) if x.count(",") > 1 else x)

unq_locations = df["Location"].unique()

try:
    location_map = {addr: geocode(addr) for addr in unq_locations}
except GeocoderServiceError as e:
    print(f"{e}")

# Extract Lat/Long into new columns using mapping
df['point'] = df['Location'].map(location_map)
df['Latitude'] = df['point'].apply(lambda loc: loc.latitude if loc else None)
df['Longitude'] = df['point'].apply(lambda loc: loc.longitude if loc else None)

# Clean up
df = df.drop(columns=['point'])
print(df)

df.to_csv("space_missions_with_coor.csv")