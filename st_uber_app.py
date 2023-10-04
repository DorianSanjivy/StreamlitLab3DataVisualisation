import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Function to load and transform data
def load_and_transform_data():
    df = pd.read_parquet("uber_good.parquet")

    df['dom'] = df['Date/Time'].str[8:10].astype(int)
    df['weekday'] = pd.to_datetime(df['Date/Time'].str[:10]).dt.weekday
    df['hour'] = df['Date/Time'].str[11:13].astype(int)

    return df


def plot_histograms(df):
    st.subheader("Histograms")

    # Frequency by Day of the Month (DoM) - Uber - April 2014
    col1, col2, col3 = st.columns(3)

    with col1:
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.hist(df['dom'], bins=30, rwidth=0.8, range=(0.5, 30.5))
        ax.set(xlabel='Day of the Month', ylabel='Frequency', title='Frequency by DoM')
        st.pyplot(fig)

    with col2:
        by_date = df.groupby('dom').apply(lambda rows: len(rows))
        fig, ax = plt.subplots(figsize=(5, 4))
        by_date.plot(kind='bar', ax=ax)
        ax.set(xlabel='Day of the Month', ylabel='Frequency', title='Unsorted')
        st.pyplot(fig)

    with col3:
        by_date_sorted = by_date.sort_values()
        fig, ax = plt.subplots(figsize=(5, 4))
        by_date_sorted.plot(kind='bar', ax=ax)
        ax.set(xlabel='Day of the Month', ylabel='Frequency', title='Sorted')
        st.pyplot(fig)

    col4, col5 = st.columns(2)

    with col4:
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.hist(df['hour'], bins=24, range=(0.5, 24))
        ax.set(xlabel='Hour of the Day', ylabel='Frequency', title='Frequency by Hour')
        st.pyplot(fig)

    with col5:
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.hist(df['weekday'], bins=7, range=(-.5, 6.5), rwidth=0.8, alpha=0.7)
        ax.set(xlabel='Weekday', ylabel='Frequency', title='Frequency by Weekday')
        st.pyplot(fig)

    # Heatmap for Weekday by Hour
    by_weekday_hour = df.groupby(['weekday', 'hour']).apply(lambda rows: len(rows)).unstack()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(by_weekday_hour, annot=False, cmap='coolwarm', fmt="d", linewidths=.5, ax=ax)
    ax.set_xlabel('Hour of the Day', fontsize=14)
    ax.set_ylabel('Weekday', fontsize=14)
    ax.set_title('Frequency by Weekday and Hour', fontsize=16)
    ax.set_yticks(range(7))
    ax.set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], rotation=0, fontsize=12)
    ax.tick_params(axis='x', labelsize=12)
    st.pyplot(fig)


def plot_lat_lon(df):
    st.subheader("Latitude & Longitude Distributions")

    # Latitude & Longitude Histograms side-by-side
    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.hist(df['Lat'], bins=100, range=(40.5, 41), color='blue', alpha=0.7)
        ax.set(xlabel='Latitude', ylabel='Frequency', title='Distribution of Latitudes')
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.hist(df['Lon'], bins=100, range=(-74.25, -73.5), color='red', alpha=0.7)
        ax.set(xlabel='Longitude', ylabel='Frequency', title='Distribution of Longitudes')
        st.pyplot(fig)

    # Combined Histogram for Latitude & Longitude
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.hist(df['Lat'], bins=100, range=(40.5, 41), color='blue', alpha=0.6, label='Latitude')
    ax1.set_xlabel('Latitude', color='blue')
    ax1.set_ylabel('Frequency')
    ax1.tick_params(axis='x', labelcolor='blue')
    ax2 = ax1.twiny()
    ax2.hist(df['Lon'], bins=100, range=(-74.25, -73.5), color='red', alpha=0.6, label='Longitude')
    ax2.set_xlabel('Longitude', color='red')
    ax2.tick_params(axis='x', labelcolor='red')
    plt.title('Distribution of Latitudes and Longitudes')
    st.pyplot(fig)

    # Scatter Plot for Latitude & Longitude
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(df['Lon'], df['Lat'], alpha=0.5, s=1)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Scatter Plot of Latitude and Longitude')
    st.pyplot(fig)

# Main Execution
def main():
    st.title('Streamlit Uber App')

    # Load and transform data
    df = load_and_transform_data()

    # Plot histograms
    plot_histograms(df)

    # Plot Latitude and Longitude
    plot_lat_lon(df)


if __name__ == "__main__":
    main()
