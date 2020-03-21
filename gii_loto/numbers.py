"""модуль для работы с номерами
"""

import os
import random

from time import sleep
from typing import Dict, Tuple, Set

import yaml

from bs4 import BeautifulSoup
from bs4.element import Tag

from gii_loto import settings
from gii_loto.helpers import log, get_browser


def __get_cache_file_path(edition: int) -> str:
    """возвращает путь к кешированному тиражу
    """
    return os.path.join(settings.LOGS_DIR, f'{edition}.html')


@log('download_edition: {edition}')
def __download_edition(edition: int, last_downloaded_edition: int) -> bool:
    """загружаем сведения по тиражу
    :param browser: браузер для загрузки данных
    :param edition: тираж
    :param last_downloaded_edition: последний загруженный тираж
    :return: возвращает результат работы,
        True - загрузил
        False - не загрузил, есть в кеше
    """

    cache_file_path = __get_cache_file_path(edition)

    if not os.path.exists(cache_file_path):
        browser = get_browser()

        browser.get(f'{settings.URL_ARCHIVE}{edition}')

        if (edition - last_downloaded_edition) == 1:
            # последовательная подгрузка тиражей
            sleep(random.randint(30, 60))

        with open(cache_file_path, 'w', encoding='utf-8') as cache_file:
            cache_file.write(browser.page_source)
    else:
        return False

    return True


@log('get parsed edition: {edition}')
def __get_parsed_edition(edition: int) -> Dict[int, int]:
    """парсим числа тиража
    :param edition: тираж
    """
    cache_file_path = __get_cache_file_path(edition)

    with open(cache_file_path, encoding='utf-8') as cache_file:
        edition_page_content = cache_file.read()

    soup = BeautifulSoup(edition_page_content, 'html.parser')

    divs = soup.find_all(settings.S_1, class_=settings.S_1_1)
    assert len(divs) == 1

    div: Tag = divs[0]

    tables: Tuple[Tag, Tag] = div.find_all(settings.S_2)
    assert len(tables) == 2

    header_t, data_t = tables

    header_tds: Tuple[Tag] = header_t.find_all(settings.S_3)
    assert len(header_tds) == 4, len(header_tds)

    tours_tr: Tuple[Tag] = data_t.find_all(settings.S_4)

    edition_numbers = set()

    for tour_tr in tours_tr:
        tour_tds: Tuple[Tag, Tag, Tag, Tag] = tour_tr.find_all(settings.S_5)
        name, numbers, ticket_counts, amount = tour_tds

        try:
            numbers = [int(n) for n in numbers.text.split()]
        except ValueError:
            if numbers.text.strip().lower() not in settings.NUMBERS_EXCLUDE_TEXTS:
                print(edition, name, numbers.text.lower())
                raise
            continue

        edition_numbers.update(numbers)

    return settings.ALL_NUMBERS.difference(edition_numbers)


@log('get_numbers')
def get_numbers() -> Dict[int, Set[int]]:
    """возвращает не выпавшие номера по тиражам
    """

    if os.path.exists(settings.NUMBERS_PATH):
        with open(settings.NUMBERS_PATH) as numbers_file:
            numbers = yaml.safe_load(numbers_file)
    else:
        numbers = {}

    browser = None

    last_downloaded_edition = 0

    require_save = False

    for edition in range(settings.FIRST_EDITION, settings.LAST_EDITION+1):

        if edition not in numbers:
            downloaded = __download_edition(
                edition=edition,
                last_downloaded_edition=last_downloaded_edition
            )
            if downloaded:
                last_downloaded_edition = edition
            numbers[edition] = __get_parsed_edition(edition=edition)
            require_save = True

    if require_save:
        save_numbers(numbers)

    return numbers


def save_numbers(numbers: Dict[int, Set[int]]):
    """сохраняет номера в кеш файл
    :param numbers: данные по номерам
    """
    with open(settings.NUMBERS_PATH, 'w') as numbers_file:
        yaml.safe_dump(numbers, numbers_file)
