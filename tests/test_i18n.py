# Import gettext module
import gettext
import os

# Set the local directory
appname = 'i18n'
localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'locales')

print(localedir)
# Set up Gettext
lang_en = gettext.translation(appname, localedir, 
                              fallback=True, languages=['es'])

# Create the "magic" function
lang_en.install()

print(lang_en)
# 

# Translate message
print(_("Hello World"))
# print(_("Learn i18n"))
print("Message Catalog:")
print(lang_en._catalog)
print("\nCharacter Set:")
print(lang_en.charset)
print("\nFallback Enabled:")
print(lang_en._fallback)
print("\nTranslator Info:")
print(lang_en.info())

# pybabel init -l fr -i locales/i18n.pot -d locales -D i18n
# pybabel init -l <...> -i locales/i18n.pot -d locales -D i18n
# pybabel init -l <...> -i locales/i18n.pot -d locales -D i18n
# pybabel compile -d locales -D i18n
# python3 tests/test_i18n.py