"""конфигурация приложения
"""

import os

import yaml

HOME_DIR = os.path.expanduser('~')
SETTINGS_DIR = os.path.join(HOME_DIR, 'gii_loto_settings')

LOGS_DIR = os.path.join(SETTINGS_DIR, 'logs')
CHROME_DRIVER_PATH = os.path.join(SETTINGS_DIR, 'chromedriver.exe')

os.makedirs(SETTINGS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# список всех номеров
ALL_NUMBERS = set(range(1, 91))
MISS_TOUR = -1
PAGE_LOAD_TIMEOUT = 10

TICKET_MAX_PERCENT_STEP = 0.01


def load():
    """загрузка конфигурации
    """
    settings_file_path = os.path.join(SETTINGS_DIR, 'settings.yaml')
    with open(settings_file_path, encoding='utf-8') as settings_file:
        custom_settings_yaml = yaml.safe_load(settings_file)

    custom_settings = {}
    globals().update(custom_settings)


load()
