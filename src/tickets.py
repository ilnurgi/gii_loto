"""билеты
"""

from time import sleep

import settings

from helpers import get_browser


def __get_lucky_tickets(browser, miss_percents):
    """возвращает счастливые билеты
    :param browser: браузер
    :param miss_percents: процентаж для чисел
    """

    div = browser.find_element_by_css_selector(settings.S_6)
    div_tickets = div.find_elements_by_css_selector(settings.S_7)
    assert len(div_tickets) == 10

    result = {}
    for div_ticket in div_tickets:
        div_ticket_number = div_ticket.find_element_by_css_selector(settings.S_8_1)
        table_trs = div_ticket.find_elements_by_css_selector(settings.S_8_2)
        assert len(table_trs) == 6
        numbers = []
        for table_tr in table_trs:
            numbers.extend(int(n) for n in table_tr.text.split())
        result[div_ticket_number.text] = (sum(miss_percents[n] for n in numbers) / len(numbers))
    return result


def get_lucky_tickets(numbers: dict, max_percent: float = settings.TICKET_MAX_PERCENT):
    """возвращает счастливые билеты
    :param numbers: сведения по числам
    :param max_percent: процентаж, ниже которой смотрим билет
    """
    # вычисляем процент не выпадания номеров
    miss_counter = {number: 0 for number in settings.ALL_NUMBERS}
    for edition, miss_edition_numbers in numbers.items():
        for miss_number in miss_edition_numbers:
            miss_counter[miss_number] += 1
    miss_percents = {
        n: (counter / settings.EDITIONS_COUNT) * 100
        for n, counter in miss_counter.items()
    }

    browser = get_browser()
    browser.get(settings.URL_TICKETS)
    input('авторизуйся')

    while True:

        browser.get(settings.URL_TICKETS)
        result = __get_lucky_tickets(browser, miss_percents)
        min_percent = min(result.values())
        print(min_percent, max_percent)

        if min_percent < max_percent:
            return result

        max_percent += settings.TICKET_MAX_PERCENT_STEP
        sleep(1)
