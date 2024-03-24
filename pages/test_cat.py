import openai
from openai import OpenAI
import streamlit as st
from typing import List

openai.api_key = st.secrets.ai["OPENAI_KEY"]
print(st.secrets.ai["OPENAI_KEY"])

# openai.Model.list() # List all OpenAI models

def get_openai_response(user_input):
    """
    This function sends the user input to OpenAI's Chat API and returns the model's response.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Specify the model for chat applications
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ]
        )
        # Extracting the text from the last response in the chat
        if response.choices:
            return response.choices[0].message['content'].strip()
        else:
            return "No response from the model."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def create_gpt_completion(ai_model: str, messages: List[dict]) -> dict:
    openai.api_key = st.secrets.ai["OPENAI_KEY"]
    completion = openai.ChatCompletion.create(
        model=ai_model,
        messages=messages,
    )
    return completion
# Print the returned output from the LLM model

client = openai

stream = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")