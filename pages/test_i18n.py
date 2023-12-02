import streamlit as st
import os
import gettext
import locale

# Ensure locale is set to the desired language
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

# Set the path to your custom directory
locale.bindtextdomain('messages', 'i18n')

# Set the domain (usually 'messages')
locale.textdomain('messages')

# Define the directory containing the translation files
# localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "locales")
localedir = os.path.join("locales")

# st.write(os.path.abspath(os.path.dirname(__file__)))

# Initialize translation based on user's choice (default is English)
def setup_translation(locale):
    t = gettext.translation("app", localedir=localedir, languages=[locale], fallback=True)
    _ = t.gettext
    return _

# Select language
language = st.selectbox("Select Language", ["en", "fr"])


st.write(language)
# Set up translations
_ = setup_translation(language)

# Translated text
translated_text = _("Hello, World!")
st.title("i18n test")
# Display translated text
st.title(translated_text)