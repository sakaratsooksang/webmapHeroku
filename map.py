"""An example of showing geographic data."""
import numpy as np
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import datetime
# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

# LOADING DATA
DATE_TIME = "timestart"
DATA_URL = (
    "https://github.com/sakaratsooksang/webmapHeroku/blob/main/data.pq?raw=true"
)

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_parquet(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data

data = load_data(100000)

# CREATING FUNCTION FOR MAPS

def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns((2,3))
start = datetime.date(2019,1,1)
stop = datetime.date(2019,1,5)
with row1_1:
    st.title("Bangkok Metropolitan Region Ridesharing Data")
    date_selected = st.slider("Select Date of Interesting", start, stop)
    hour_selected = st.slider("Select hour of pickup", 0, 23)
    

with row1_2:
    st.write(
    """
    ##
    Author : Sakarat Sooksang 6130824521
    """)
    st.write(
    """
    Data Science Assignment : Web application creation Using Streamlit.
    """)
    st.write(
    """
    Source Code : https://share.streamlit.io/streamlit/demo-uber-nyc-pickups/
    """)
    st.write(
    """
    GitHub Repository :https://github.com/sakaratsooksang/webmapHeroku
    """)
    st.write(
    """
    Deploy by Heroku.
    """)
# FILTERING DATA BY HOUR SELECTED
data = data[(data[DATE_TIME].dt.date == date_selected) & (data[DATE_TIME].dt.hour == hour_selected)]
# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row2= st.columns((5))

# SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
zoom_level = 12
midpoint = (np.average(data["lat"]), np.average(data["lon"]))

st.write("**Bangkok Metropolitan Region from %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
map(data, midpoint[0], midpoint[1], 11)

# FILTERING DATA FOR THE HISTOGRAM
filtered = data[
    (data[DATE_TIME].dt.hour >= hour_selected) & (data[DATE_TIME].dt.hour < (hour_selected + 1))
    ]

hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

chart_data = pd.DataFrame({"minute": range(60), "pickups": hist})

# LAYING OUT THE HISTOGRAM SECTION

st.write("")

st.write("**Breakdown of rides per minute between %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))

st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ).configure_mark(
        opacity=0.5,
        color='orange'
    ), use_container_width=True)