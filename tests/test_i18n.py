# Import gettext module
import gettext

# Set the local directory
appname = 'i18n'
localedir = '../locales'

# Set up Gettext
en_i18n = gettext.translation(appname, localedir, fallback=True, languages=['en'])

# Create the "magic" function
en_i18n.install()

# Translate message
print(_("Hello World"))

#  2815  xgettext -d base -o ../locales/i18n.pot test_i18n.py\n
#  2817  code ../locales/en/LC_MESSAGES/i18n.po
#  2821  msgfmt -o ../locales/en/LC_MESSAGES/i18n.mo ../locales/en/LC_MESSAGES/i18n.po
#  2822  python3 test_i18n.py