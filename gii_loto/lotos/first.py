"""первая лотерея
"""
from typing import Tuple

from bs4 import Tag

from gii_loto.lotos.base import BaseLoto


class FirstLoto(BaseLoto):
    """первая лотерея
    """
    CONFIG_FILE_NAME = 'first_loto.yaml'
    LOTO_NAME = 'first_loto'

    def _get_data_table(self, data_div: Tag):
        """возвращает элемент таблицы с данными
        """

        tables: Tuple[Tag, Tag] = data_div.find_all(self.S_2)
        assert len(tables) == 2, len(tables)

        header_t, data_t = tables

        header_tds: Tuple[Tag] = header_t.find_all(self.S_3)
        assert len(header_tds) == 4, len(header_tds)

        return data_t

    def _get_numbers(self, tour_tr: Tag, edition: int) -> list:
        """возвращает данные тура
        """
        tour_tds: Tuple[Tag, Tag, Tag, Tag] = tour_tr.find_all(self.S_5)

        name, numbers, ticket_counts, amount = tour_tds
        try:
            numbers = [int(n) for n in numbers.text.split()]
        except ValueError:
            if not any(
                    exclude in numbers.text.strip().lower()
                    for exclude in self.NUMBERS_EXCLUDE_TEXTS_IN
            ):
                print(edition, name, numbers.text.lower())
                raise

        return numbers
