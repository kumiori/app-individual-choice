import gettext
import os

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
translate = gettext.translation('i18n', localedir, fallback=True)
_ = translate.gettext

_('Close the underscore function first. A {number}').format(number=42)


