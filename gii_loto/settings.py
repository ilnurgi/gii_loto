"""конфигурация приложения
"""

import os

import yaml

HOME_DIR = os.path.expanduser('~')
SETTINGS_DIR = os.path.join(HOME_DIR, 'gii_loto_settings')

LOGS_DIR = os.path.join(SETTINGS_DIR, 'logs')
NUMBERS_PATH = os.path.join(LOGS_DIR, 'numbers.yaml')
CHROME_DRIVER_PATH = os.path.join(SETTINGS_DIR, 'chromedriver.exe')

os.makedirs(SETTINGS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# период тиражей
FIRST_EDITION = 0
LAST_EDITION = 0

# список всех номеров
ALL_NUMBERS = set(range(1, 91))
MISS_TOUR = -1

# урл страницы с данными
URL_ARCHIVE = ''

# урл с билетами
URL_TICKETS = ''

TOUR_NUMBER_MISS_TEXT = ''

NUMBERS_EXCLUDE_TEXTS = []

TICKET_MAX_PERCENT = 5
TICKET_MAX_PERCENT_STEP = 0.01

# селекторы для парсинга страниц
S_1 = ''
S_1_1 = ''
S_2 = ''
S_3 = ''
S_4 = ''
S_5 = ''
S_6 = ''
S_7 = ''
S_8_1 = ''
S_8_2 = ''


def load():
    """загрузка конфигурации
    """
    settings_file_path = os.path.join(SETTINGS_DIR, 'settings.yaml')
    with open(settings_file_path, encoding='utf-8') as settings_file:
        custom_settings_yaml = yaml.safe_load(settings_file)

    custom_settings = {
        key: custom_settings_yaml[key]
        for key in (
            'FIRST_EDITION', 'LAST_EDITION', 'TOUR_NUMBER_MISS_TEXT', 'NUMBERS_EXCLUDE_TEXTS', 'CHROME_DRIVER_PATH',
            'URL_ARCHIVE', 'URL_TICKETS', 'TICKET_MAX_PERCENT', 'TICKET_MAX_PERCENT_STEP',
            'S_1', 'S_1_1', 'S_2', 'S_3', 'S_4', 'S_5', 'S_6', 'S_7', 'S_8_1', 'S_8_2',
        ) if key in custom_settings_yaml
    }
    globals().update(custom_settings)


load()

EDITIONS = tuple(range(FIRST_EDITION, LAST_EDITION + 1))
EDITIONS_COUNT = len(EDITIONS)
