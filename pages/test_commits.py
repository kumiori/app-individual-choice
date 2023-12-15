import streamlit as st
import requests
import xml.etree.ElementTree as ET
import random
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def fetch_xml_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for errors
        return response.text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching XML data: {e}")
        return None

def parse_commit_feed(xml_data):
    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Extract relevant information from each entry
    commits = []
    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        commit_id = entry.find('{http://www.w3.org/2005/Atom}id').text
        commit_id_full = entry.find('{http://www.w3.org/2005/Atom}id').text
        commit_id = commit_id_full.split("/")[-1]  # Extract the commit number
        link = entry.find('{http://www.w3.org/2005/Atom}link[@rel="alternate"]').attrib['href']
        title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
        updated = entry.find('{http://www.w3.org/2005/Atom}updated').text
        author_name = entry.find('.//{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name').text
        content_element = entry.find('{http://www.w3.org/2005/Atom}content')
        content = content_element.text.strip() if content_element is not None else ""

        commits.append({
            'commit_id': commit_id,
            'link': link,
            'title': title,
            'updated': updated,
            'author_name': author_name,
            'content': content
        })

    return commits

# Streamlit app
st.title("GitHub Commit Feed Viewer")

# Example GitHub repository XML feed URL
github_repo_url = "https://github.com/kumiori/mec647/commits/main.atom"

# Fetch XML data
xml_data = fetch_xml_data(github_repo_url)

# If XML data is successfully fetched, display the commits
if xml_data:
    commits = parse_commit_feed(xml_data)

    # Filter commits with titles containing "#"
    hash_commits = [commit for commit in commits if "#" in commit['title']]
    print(hash_commits)
    # Display filtered commits
    st.header("Commits with '#' in Title")
    for commit in hash_commits:
        st.write(f"Commit ID: {commit['commit_id']}")
        # st.write(f"Link: {commit['link']}")
        st.write(f"Title: {commit['title']}")
        st.write(f"Updated: {commit['updated']}")
        # st.write(f"Author: {commit['author_name']}")
        # st.write(f"Content: {commit['content']}")
        st.markdown("---")  # Add a separator between commits

    # Display one random commit
    st.header("Random Commit")
    random_commit = random.choice(commits)
    st.write(f"Commit ID: {random_commit['commit_id']}")
    st.write(f"Link: {random_commit['link']}")
    st.write(f"Title: {random_commit['title']}")
    st.write(f"Updated: {random_commit['updated']}")
    st.write(f"Author: {random_commit['author_name']}")
    st.write(f"Content: {random_commit['content']}")

    # Create a heartbeat or brain signal plot using plotly.express
    st.header("Heartbeat or Brain Signal Visualization")

    # Generate a sample dataframe for demonstration
    df = pd.DataFrame({
        'Time': np.arange(0, 10, 0.1),
        'Signal': np.sin(np.arange(0, 10, 0.1)) + np.random.normal(scale=0.3, size=100)
    })

    # Create the plot
    # fig = px.line(df, x='Time', y='Signal', labels={'Signal': 'Amplitude'})
    # fig.update_layout(title_text='Heartbeat or Brain Signal', xaxis_title='Time', yaxis_title='Amplitude')

    # Create the plot
    fig = px.line(df, x='Time', y='Signal', labels={'Signal': 'Amplitude'})
    
    # Get the timestamps of the commits
    commit_timestamps = [pd.to_datetime(commit['updated']).timestamp() for commit in commits]

    # Rescale the commit dates by the length of a year
    year_length = 365 * 24 * 60 * 60  # seconds in a year
    rescaled_commit_times = [(timestamp - min(commit_timestamps)) / year_length for timestamp in commit_timestamps]

    # Draw red dots at the rescaled commit times
    for rescaled_time in rescaled_commit_times:
        fig.add_trace(go.Scatter(x=[rescaled_time], y=[0], mode='markers', marker=dict(color='red')))

    # Update layout to remove axis numbers and labels
    fig.update_layout(
        showlegend=False,
        xaxis=dict(showline=False, showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showline=False, showgrid=False, zeroline=False, showticklabels=False),
    )

    # Display the plot
    st.plotly_chart(fig)