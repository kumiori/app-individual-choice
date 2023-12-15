import xml.etree.ElementTree as ET

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

# Example XML data (replace this with your actual XML data)
xml_data = """
... (your XML data here) ...
"""

# Parse the XML data and get a list of commits
commits = parse_commit_feed(xml_data)

# Example: Print information about each commit
for commit in commits:
    print(f"Commit ID: {commit['commit_id']}")
    print(f"Link: {commit['link']}")
    print(f"Title: {commit['title']}")
    print(f"Updated: {commit['updated']}")
    print(f"Author: {commit['author_name']}")
    print(f"Content: {commit['content']}")
    print("\n")
