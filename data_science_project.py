import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the application
st.title('Zomato Data Analysis')

# File upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load data
    dataframe = pd.read_csv(uploaded_file)
    
    # Function to handle rate column
    def handleRate(value):
        value = str(value).split('/')
        value = value[0]
        try:
            return float(value)
        except:
            return None

    dataframe['rate'] = dataframe['rate'].apply(handleRate)
    dataframe.dropna(subset=['rate'], inplace=True)

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    options = st.sidebar.multiselect(
        'Select analysis to perform:',
        ['Explore listed_in (type) column', 
         'Preferred by a larger number of individuals', 
         'Restaurant with maximum votes', 
         'Explore online_order column', 
         'Explore ratings',
         'Compare online and offline order ratings',
         'Heatmap of listed_in(type) and online_order']
    )

    # Explore listed_in (type) column
    if 'Explore listed_in (type) column' in options:
        st.subheader('Explore by Type of Restaurant')
        fig, ax = plt.subplots(figsize=(10, 6))
        dataframe['listed_in(type)'].value_counts().plot(kind='bar', ax=ax)
        ax.set_xlabel("Type of restaurant")
        ax.set_ylabel("Count")
        ax.set_title("Number of Restaurants by Type")
        st.pyplot(fig)

    # Preferred by a larger number of individuals
    if 'Preferred by a larger number of individuals' in options:
        st.subheader('Preferred by a Larger Number of Individuals')
        grouped_data = dataframe.groupby('listed_in(type)')['votes'].sum()
        fig, ax = plt.subplots(figsize=(10, 6))
        grouped_data.plot(kind='line', marker='o', color='green', ax=ax)
        ax.set_xlabel("Type of restaurant")
        ax.set_ylabel("Votes")
        ax.set_title("Total Votes by Restaurant Type")
        st.pyplot(fig)

    # Restaurant with maximum votes
    if 'Restaurant with maximum votes' in options:
        st.subheader('Restaurant with Maximum Votes')
        max_votes = dataframe['votes'].max()
        restaurant_with_max_votes = dataframe.loc[dataframe['votes'] == max_votes, 'name']
        st.write("Restaurant(s) with the maximum votes:")
        st.write(restaurant_with_max_votes)

    # Explore online_order column
    if 'Explore online_order column' in options:
        st.subheader('Explore Online Orders')
        fig, ax = plt.subplots(figsize=(10, 6))
        dataframe['online_order'].value_counts().plot(kind='bar', ax=ax)
        ax.set_xlabel("Online Order")
        ax.set_ylabel("Count")
        ax.set_title("Number of Restaurants with Online Orders")
        st.pyplot(fig)

    # Explore ratings
    if 'Explore ratings' in options:
        st.subheader('Explore by Ratings')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(dataframe['rate'], bins=5, edgecolor='black')
        ax.set_xlabel("Rating")
        ax.set_ylabel("Frequency")
        ax.set_title("Distribution of Ratings")
        st.pyplot(fig)

    # Compare online and offline order ratings
    if 'Compare online and offline order ratings' in options:
        st.subheader('Compare Online and Offline Order Ratings')
        fig, ax = plt.subplots(figsize=(10, 6))
        dataframe.boxplot(column='rate', by='online_order', ax=ax)
        ax.set_xlabel("Online Order")
        ax.set_ylabel("Rating")
        ax.set_title("Ratings by Online Order")
        fig.suptitle("")  # Suppress default title
        st.pyplot(fig)

    # Heatmap of listed_in(type) and online_order
    if 'Heatmap of listed_in(type) and online_order' in options:
        st.subheader('Heatmap of Listed In (Type) and Online Order')
        pivot_table = dataframe.pivot_table(index='listed_in(type)', columns='online_order', aggfunc='size', fill_value=0)
        fig, ax = plt.subplots(figsize=(12, 8))
        cax = ax.imshow(pivot_table, cmap='YlGnBu', interpolation='nearest')
        fig.colorbar(cax, ax=ax, label='Count')
        ax.set_xticks(range(len(pivot_table.columns)))
        ax.set_xticklabels(pivot_table.columns)
        ax.set_yticks(range(len(pivot_table.index)))
        ax.set_yticklabels(pivot_table.index)
        ax.set_xlabel("Online Order")
        ax.set_ylabel("Listed In (Type)")
        ax.set_title("Heatmap of Restaurant Types and Online Orders")
        st.pyplot(fig)

else:
    st.info('Please upload a CSV file to get started.')
