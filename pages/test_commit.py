import streamlit as st
import requests
import git
import json
import streamlit as st
import requests
import xml.etree.ElementTree as ET


def fetch_xml_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for errors
        return response.text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching XML data: {e}")
        return None

# Function to fetch Git commit messages
def get_commits(repo_path):
    repo = git.Repo(repo_path)
    commits = [{'message': commit.message, 'author': commit.author.name} for commit in repo.iter_commits()]
    return commits

# Function to store commits in a GitHub Gist
def store_commits_on_gist(commits):
    gist_data = {
        'description': 'Git Commit Messages',
        'public': True,
        'files': {'commits.json': {'content': json.dumps(commits)}}
    }

    response = requests.post('https://api.github.com/gists', json=gist_data)

    if response.status_code == 201:
        gist_url = response.json()['html_url']
        return gist_url
    else:
        return None

# Main Streamlit app
st.title('Git Commit Messages')

def parse_commit_feed(xml_data):
    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Extract relevant information from each entry
    commits = []
    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        commit_id = entry.find('{http://www.w3.org/2005/Atom}id').text
        link = entry.find('{http://www.w3.org/2005/Atom}link[@rel="alternate"]').attrib['href']
        title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
        updated = entry.find('{http://www.w3.org/2005/Atom}updated').text
        author_name = entry.find('.//{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name').text
        content = entry.find('{http://www.w3.org/2005/Atom}content').text.strip()

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

    # Display information about each commit
    for commit in commits:
        st.write(f"Commit ID: {commit['commit_id']}")
        st.write(f"Link: {commit['link']}")
        st.write(f"Title: {commit['title']}")
        st.write(f"Updated: {commit['updated']}")
        st.write(f"Author: {commit['author_name']}")
        st.write(f"Content: {commit['content']}")
        st.markdown("---")  # Add a separator between commits




