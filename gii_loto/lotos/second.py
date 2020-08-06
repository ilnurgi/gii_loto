"""вторая лотерея
"""
from typing import Tuple

from bs4 import Tag

from gii_loto.lotos.base import BaseLoto


class SecondLoto(BaseLoto):
    """вторая лотерея
    """
    CONFIG_FILE_NAME = 'second_loto.yaml'
    LOTO_NAME = 'second_loto'

    def _get_data_table(self, data_div: Tag):
        """возвращает элемент таблицы с данными
        """

        tables: Tuple[Tag, Tag] = data_div.find_all(self.S_2)
        assert len(tables) == 1, len(tables)

        data_t = tables[0]

        return data_t

    def _get_numbers(self, tour_tr: Tag, edition: int) -> list:
        """возвращает данные тура
        """
        tour_ths: Tuple[Tag, Tag, Tag, Tag] = tour_tr.find_all(self.S_3)
        tour_tds: Tuple[Tag, Tag, Tag, Tag] = tour_tr.find_all(self.S_5)
        if not tour_ths and not tour_tds:
            assert False
        elif not tour_tds:
            return []

        name, numbers, ticket_counts, amount = tour_tds
        try:
            numbers = [int(n) for n in numbers.text.split(',') if n.strip()]
        except ValueError:
            if not any(exclude in numbers.text.strip().lower() for exclude in self.NUMBERS_EXCLUDE_TEXTS):
                print(edition, name, numbers.text.lower())
                raise

        return numbers
