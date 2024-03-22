import os
import streamlit as st
from datetime import datetime

def list_files_by_modified_date(directory="."):
    files = os.listdir(directory)
    py_files = [file for file in files if file.endswith(".py") and file != "__init__.py"]

    files_with_timestamp = [(file, os.path.getmtime(os.path.join(directory, file))) for file in py_files]
    sorted_files = sorted(files_with_timestamp, key=lambda x: x[1], reverse=True)
    return sorted_files

def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def main():
    st.title("Recent Work")
    st.write("List of files in the current directory sorted by modified date (newest first):")

    pages_directory = os.path.join(os.getcwd(), "pages")
    files = list_files_by_modified_date(pages_directory)

    for file, timestamp in files:
        formatted_timestamp = format_timestamp(timestamp)
        # st.write(f"- {file} (last modified: {formatted_timestamp})")
        page_label = f"{file} (last modified: {formatted_timestamp})"
        # st.page_link("pages/", label=page_label)
        # print("pages/"+file)
        st.page_link("pages/"+file, label=page_label)

if __name__ == "__main__":
    main()
