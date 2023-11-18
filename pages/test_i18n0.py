import streamlit as st
import os
import gettext

# Define a dictionary for supported languages and their locales
languages = {
    "English": "en_US",
    "French": "fr_FR"
}

# Create a language selection dropdown
selected_lang = st.selectbox("Select a language", list(languages.keys()))

# Set the path to your custom directory
custom_locale_directory = 'i18n'

def setup_translation(locale):
    t = gettext.translation("app", localedir=custom_locale_directory, languages=[locale], fallback=True)
    _ = t.gettext
    return _

_ = setup_translation(languages[selected_lang])

# Load the translation object for the selected language
translation = gettext.translation('messages', localedir=custom_locale_directory, languages=[languages[selected_lang]])
translation.install()

def translate_text(text):
    return translation.gettext(text)

# Your app content
st.title(translate_text("Streamlit Internationalization Example"))
st.write(translate_text("This is a multilingual Streamlit app."))

# Here, use translate_text() to translate text in your app
st.write(translate_text("Select your preferred language:"))

# Language switch
if selected_lang != "English":
    st.write(translate_text("You are using the French version."))
else:
    st.write(translate_text("You are using the English version."))

st.write(_("Hello, world"))
# Other app content