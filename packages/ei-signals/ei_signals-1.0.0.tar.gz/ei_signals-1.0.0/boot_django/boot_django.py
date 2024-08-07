import os
import django


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../ei_signals"))


def boot_django():
    import ei_signals.settings
 
    django.setup()