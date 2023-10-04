# streamlit run st_ny_trips_app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk
import missingno as msno

st.set_page_config(layout="wide")  # Setting the page layout to wide
st.title('Streamlit New York Trips App')

path2 = "https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv"
df2 = pd.read_csv(path2)

# Missing data plot
with st.container():
    st.subheader("Visualisation des données manquantes")
    msno.bar(df2)
    st.pyplot(plt)

# Convert date columns to datetime
df2['tpep_pickup_datetime'] = pd.to_datetime(df2['tpep_pickup_datetime'])
df2['tpep_dropoff_datetime'] = pd.to_datetime(df2['tpep_dropoff_datetime'])

# Plot histograms
with st.container():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        plt.figure(figsize=(10, 6))
        plt.hist(df2['trip_distance'], bins=50, range=(0, 20), color='blue', edgecolor='black')
        plt.title('Distribution des distances de trajet')
        plt.xlabel('Distance (miles)')
        plt.ylabel('Fréquence')
        plt.grid(True)
        st.pyplot(plt)

    with col2:
        plt.figure(figsize=(10, 6))
        plt.hist(df2['fare_amount'], bins=50, range=(0, 60), color='green', edgecolor='black')
        plt.title('Distribution des montants de la course')
        plt.xlabel('Montant de la course ($)')
        plt.ylabel('Fréquence')
        plt.grid(True)
        st.pyplot(plt)

    with col3:
        plt.figure(figsize=(10, 6))
        plt.hist(df2['tip_amount'], bins=50, range=(0, 20), color='red', edgecolor='black')
        plt.title('Distribution des pourboires')
        plt.xlabel('Pourboire ($)')
        plt.ylabel('Fréquence')
        plt.grid(True)
        st.pyplot(plt)

    with col4:
        plt.figure(figsize=(10, 6))
        plt.hist(df2['passenger_count'], bins=50, color='purple', edgecolor='black')
        plt.title('Distribution du nombre de passagers par trajet')
        plt.xlabel('Nombre de passagers')
        plt.ylabel('Fréquence')
        plt.grid(True)
        st.pyplot(plt)

# Pickup & Dropoff data preparations
df2['pickup_hour'] = df2['tpep_pickup_datetime'].dt.hour
df2['pickup_weekday'] = df2['tpep_pickup_datetime'].dt.weekday
day_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
df2['pickup_weekday_str'] = df2['pickup_weekday'].map(day_map)
by_hour = df2.groupby('pickup_hour').apply(len)
by_weekday_str = df2.groupby('pickup_weekday_str').apply(len)

df2['dropoff_hour'] = df2['tpep_dropoff_datetime'].dt.hour
df2['dropoff_weekday'] = df2['tpep_dropoff_datetime'].dt.weekday
df2['dropoff_weekday_str'] = df2['dropoff_weekday'].map(day_map)
by_hour_dropoff = df2.groupby('dropoff_hour').apply(len)
by_weekday_str_dropoff = df2.groupby('dropoff_weekday_str').apply(len)

# Pickup & Dropoff plots
with st.container():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        plt.figure(figsize=(12, 6))
        plt.bar(by_hour.index, by_hour.values)
        plt.xlabel('Heure du jour')
        plt.ylabel('Nombre de courses')
        plt.title('Nombre de courses par heure')
        st.pyplot(plt)

    with col2:
        plt.figure(figsize=(12, 6))
        plt.bar(by_hour_dropoff.index, by_hour_dropoff.values, color='orange')
        plt.xlabel('Heure du jour')
        plt.ylabel('Nombre de courses')
        plt.title('Nombre de courses par heure (Dropoff)')
        st.pyplot(plt)

    with col3:
        plt.figure(figsize=(12, 6))
        plt.bar(by_weekday_str.index, by_weekday_str.values, color='blue')
        plt.xlabel('Jour de la semaine')
        plt.ylabel('Nombre de courses')
        plt.title('Nombre de courses par jour de la semaine (Pickup)')
        st.pyplot(plt)

    with col4:
        plt.figure(figsize=(12, 6))
        plt.bar(by_weekday_str_dropoff.index, by_weekday_str_dropoff.values, color='red')
        plt.xlabel('Jour de la semaine')
        plt.ylabel('Nombre de courses')
        plt.title('Nombre de courses par jour de la semaine (Dropoff)')
        st.pyplot(plt)

# Geographic Distribution plot
with st.container():
    plt.figure(figsize=(12,6))
    plt.scatter(df2['pickup_longitude'], df2['pickup_latitude'], color='blue', label='Pickup', s=1)
    plt.scatter(df2['dropoff_longitude'], df2['dropoff_latitude'], color='red', label='Dropoff', s=1)
    plt.title('Distribution géographique des points de ramassage et de dépôt')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    st.pyplot(plt)

# PyDeck plot
with st.container():
    # Create layers
    pickup_layer = pdk.Layer(
        'ScatterplotLayer',
        data=df2,
        get_position=['pickup_longitude', 'pickup_latitude'],
        get_radius=10,
        get_fill_color=[255, 0, 0, 100],  # red color
        pickable=True
    )

    dropoff_layer = pdk.Layer(
        'ScatterplotLayer',
        data=df2,
        get_position=['dropoff_longitude', 'dropoff_latitude'],
        get_radius=10,
        get_fill_color=[0, 0, 255, 100],  # blue color
        pickable=True
    )

    # Visualize the layers on the map
    view_state = pdk.ViewState(latitude=40.7, longitude=-73.9, zoom=10)
    deck = pdk.Deck(layers=[pickup_layer, dropoff_layer], initial_view_state=view_state)

    # Display the map in Streamlit
    st.pydeck_chart(deck)


