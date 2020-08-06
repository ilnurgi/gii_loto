"""базовая лотерея
"""

import os
import random

from bs4 import BeautifulSoup, Tag
from selenium.common.exceptions import TimeoutException
from time import sleep

from typing import Dict, Set, Tuple

import yaml
from selenium.webdriver.remote.webdriver import WebDriver

from gii_loto import settings
from gii_loto.helpers import log


class BaseLoto:
    """базовая лотерея
    """

    CONFIG_FILE_NAME = None
    NUMBERS_FILE = 'numbers.yaml'
    LOTO_NAME = None

    CONFIG_LOAD_KEYS = (
        'NUMBERS_PATH', 'FIRST_EDITION', 'LAST_EDITION', 'URL_ARCHIVE', 'TICKET_MAX_PERCENT',
        'URL_TICKETS', 'NUMBERS_EXCLUDE_TEXTS', 'TICKET_MAX_PERCENT',
        'S_1', 'S_1_1', 'S_2', 'S_3', 'S_4', 'S_5', 'S_6', 'S_7', 'S_8_1', 'S_8_2',
    )

    NUMBERS_PATH = None
    FIRST_EDITION = None
    LAST_EDITION = None
    URL_ARCHIVE = None
    TICKET_MAX_PERCENT = None
    URL_TICKETS = None
    NUMBERS_EXCLUDE_TEXTS = None
    S_1 = None
    S_1_1 = None
    S_2 = None
    S_3 = None
    S_4 = None
    S_5 = None
    S_6 = None
    S_7 = None
    S_8_1 = None
    S_8_2 = None

    def __init__(self, browser: WebDriver):
        """иницализация
        """
        self.browser = browser
        self.numbers = {}

        assert self.CONFIG_FILE_NAME is not None, 'CONFIG_FILE_NAME must be set'
        assert self.LOTO_NAME is not None, 'LOTO_NAME must be set'

        self.LOGS_DIR = os.path.join(settings.LOGS_DIR, self.LOTO_NAME)
        os.makedirs(self.LOGS_DIR, exist_ok=True)

        self.NUMBERS_PATH = os.path.join(self.LOGS_DIR, self.NUMBERS_FILE)

        self._load_config_file()

        self.EDITIONS = tuple(range(self.FIRST_EDITION, self.LAST_EDITION + 1))
        self.EDITIONS_COUNT = len(self.EDITIONS)

    def _load_config_file(self):
        """загрузка конфиг файла
        """

        config_file_path = os.path.join(settings.SETTINGS_DIR, self.CONFIG_FILE_NAME)
        assert os.path.exists(config_file_path), f'CONFIG_FILE not exists: {config_file_path}'

        with open(config_file_path, encoding='utf-8') as config_fh:
            config = yaml.safe_load(config_fh)

        for key, value in config.items():
            if key not in self.CONFIG_LOAD_KEYS:
                continue
            setattr(self, key, value)

    @log('get_numbers')
    def collect_numbers(self):
        """возвращает не выпавшие номера по тиражам
        """

        self.numbers.clear()

        if os.path.exists(self.NUMBERS_PATH):
            with open(self.NUMBERS_PATH) as numbers_file:
                self.numbers.update(yaml.safe_load(numbers_file))

        last_downloaded_edition = 0

        require_save = False

        for edition in range(self.FIRST_EDITION, self.LAST_EDITION + 1):

            if edition not in self.numbers:
                downloaded = self.__download_edition(
                    edition=edition,
                    last_downloaded_edition=last_downloaded_edition
                )
                if downloaded:
                    last_downloaded_edition = edition
                self.numbers[edition] = self.__get_parsed_edition(edition=edition)
                require_save = True

        if require_save:
            self.save_numbers(self.numbers)

    @log('download_edition: {edition}')
    def __download_edition(self, edition: int, last_downloaded_edition: int) -> bool:
        """загружаем сведения по тиражу
        :param browser: браузер для загрузки данных
        :param edition: тираж
        :param last_downloaded_edition: последний загруженный тираж
        :return: возвращает результат работы,
            True - загрузил
            False - не загрузил, есть в кеше
        """

        cache_file_path = self.__get_cache_file_path(edition)

        if not os.path.exists(cache_file_path):
            self.browser.get(f'{self.URL_ARCHIVE}{edition}')

            if (edition - last_downloaded_edition) == 1:
                # последовательная подгрузка тиражей
                sleep(random.randint(30, 60))

            with open(cache_file_path, 'w', encoding='utf-8') as cache_file:
                cache_file.write(self.browser.page_source)
        else:
            return False

        return True

    def _get_data_table(self, data_div: Tag):
        """возвращает таблицу данных
        """
        raise NotImplementedError()

    def _get_numbers(self, tour_tr: Tag, edition: int) -> list:
        """возвращает числа тура
        """
        raise NotImplementedError()

    @log('get parsed edition: {edition}')
    def __get_parsed_edition(self, edition: int) -> Dict[int, int]:
        """парсим числа тиража
        :param edition: тираж
        """
        cache_file_path = self.__get_cache_file_path(edition)

        with open(cache_file_path, encoding='utf-8') as cache_file:
            edition_page_content = cache_file.read()

        soup = BeautifulSoup(edition_page_content, 'html.parser')

        divs = soup.find_all(self.S_1, class_=self.S_1_1)
        assert len(divs) == 1, len(divs)

        data_t = self._get_data_table(divs[0])

        tours_tr: Tuple[Tag] = data_t.find_all(self.S_4)

        edition_numbers = set()

        for tour_tr in tours_tr:
            numbers = self._get_numbers(tour_tr, edition)
            edition_numbers.update(numbers)

        return settings.ALL_NUMBERS.difference(edition_numbers)

    def __get_cache_file_path(self, edition: int) -> str:
        """возвращает путь к кешированному тиражу
        """
        return os.path.join(self.LOGS_DIR, f'{edition}.html')

    def save_numbers(self, numbers: Dict[int, Set[int]]):
        """сохраняет номера в кеш файл
        :param numbers: данные по номерам
        """
        with open(self.NUMBERS_PATH, 'w') as numbers_file:
            yaml.safe_dump(numbers, numbers_file)

    def __get_lucky_tickets(self, miss_percents):
        """возвращает счастливые билеты
        :param miss_percents: процентаж для чисел
        """

        div = self.browser.find_element_by_css_selector(self.S_6)
        div_tickets = div.find_elements_by_css_selector(self.S_7)
        assert len(div_tickets) == 10

        result = {}
        for div_ticket in div_tickets:
            div_ticket_number = div_ticket.find_element_by_css_selector(self.S_8_1)
            table_trs = div_ticket.find_elements_by_css_selector(self.S_8_2)
            assert len(table_trs) == 6
            numbers = []
            for table_tr in table_trs:
                numbers.extend(int(n) for n in table_tr.text.split())
            result[div_ticket_number.text] = (sum(miss_percents[n] for n in numbers) / len(numbers))
        return result

    def get_lucky_tickets(self):
        """возвращает счастливые билеты
        """
        # вычисляем процент не выпадания номеров
        miss_counter = {number: 0 for number in settings.ALL_NUMBERS}
        for edition, miss_edition_numbers in self.numbers.items():
            for miss_number in miss_edition_numbers:
                miss_counter[miss_number] += 1
        miss_percents = {
            n: (counter / self.EDITIONS_COUNT) * 100
            for n, counter in miss_counter.items()
        }

        self.browser.get(self.URL_TICKETS)
        input('авторизуйся')
        max_percent = self.TICKET_MAX_PERCENT
        while True:

            self.browser.get(self.URL_TICKETS)
            result = self.__get_lucky_tickets(miss_percents)
            min_percent = min(result.values())
            print(min_percent, max_percent)

            if min_percent < max_percent:
                return result

            max_percent += settings.TICKET_MAX_PERCENT_STEP
            sleep(1)
