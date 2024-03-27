import streamlit as st
import os
import gettext
import locale

# Ensure locale is set to the desired language
# locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

# Set the path to your custom directory
# locale.bindtextdomain('messages', 'i18n')

# Set the domain (usually 'messages')
# locale.textdomain('messages')

# Define the directory containing the translation files
# localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "locales")
localedir = os.path.join("locales")

# st.write(os.path.abspath(os.path.dirname(__file__)))

# Initialize translation based on user's choice (default is English)
def setup_translation(locale):
    t = gettext.translation("loka", localedir=localedir, languages=[locale], fallback=True)
    _ = t.gettext
    return _

# Select language
language = st.selectbox("Select Language", ["en", "fr", "es"])


# Set up translations
_ = setup_translation(language)

# Translated text
translated_text = _("Hello, World!")
st.title("i18n test")
# Display translated text
st.title(translated_text)


# pybabel extract -F babel.cfg -o locales/loka.pot .

# (virtual) pybabel extract pages/test_i18n.py -o locales/loka.pot
# extracting messages from pages/test_i18n.py
# writing PO template file to locales/loka.pot
# (virtual) pybabel init -l es -i locales/loka.pot -d locales -D loka               
# creating catalog locales/es/LC_MESSAGES/loka.po based on locales/loka.pot
# (virtual) pybabel init -l fr -i locales/loka.pot -d locales -D loka
# creating catalog locales/fr/LC_MESSAGES/loka.po based on locales/loka.pot
# (virtual) pybabel init -l en -i locales/loka.pot -d locales -D loka
# creating catalog locales/en/LC_MESSAGES/loka.po based on locales/loka.pot
# (virtual) pybabel compile -d locales -D loka                       
# compiling catalog locales/fr/LC_MESSAGES/loka.po to locales/fr/LC_MESSAGES/loka.mo
# compiling catalog locales/es/LC_MESSAGES/loka.po to locales/es/LC_MESSAGES/loka.mo
# compiling catalog locales/en/LC_MESSAGES/loka.po to locales/en/LC_MESSAGES/loka.mo