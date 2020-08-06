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
PAGE_LOAD_TIMEOUT = 20

TICKET_MAX_PERCENT_STEP = 0.01


__load_keys = ()


def create_example_settings():
    """создаем пример файлов настроек
    """
    example_path = os.path.join(SETTINGS_DIR, 'example_settings.yaml')
    if os.path.exists(example_path):
        return

    yaml.dump(dict.fromkeys(__load_keys), open(os.path.join(example_path), 'w'))


def load():
    """загрузка конфигурации
    """
    settings_file_path = os.path.join(SETTINGS_DIR, 'settings.yaml')
    with open(settings_file_path, encoding='utf-8') as settings_file:
        custom_settings_yaml = yaml.safe_load(settings_file)

    custom_settings = {
        key: custom_settings_yaml[key]
        for key in __load_keys if key in custom_settings_yaml
    }
    globals().update(custom_settings)


load()
create_example_settings()
