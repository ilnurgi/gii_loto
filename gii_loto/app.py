"""приложение
"""

from pprint import pprint

from selenium import webdriver

from gii_loto import settings
from gii_loto.lotos.first import FirstLoto
from gii_loto.lotos.second import SecondLoto
from gii_loto.plotter import create_plot


def main():
    """точка входа
    """

    browser = webdriver.Chrome(settings.CHROME_DRIVER_PATH)
    browser.set_page_load_timeout(settings.PAGE_LOAD_TIMEOUT)

    loto = FirstLoto(browser)
    # loto = SecondLoto(browser)

    loto.collect_numbers()

    # рисуем диаграммы распределния номеров
    create_plot(loto)

    # получаем счастливые билеты
    tickets = loto.get_lucky_tickets()

    pprint(sorted(tickets.items(), key=lambda item: item[1], reverse=True))
    input('готово')


if __name__ == '__main__':
    main()
