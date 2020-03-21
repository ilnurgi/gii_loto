"""приложение
"""

from pprint import pprint

from loto_numbers import get_numbers
from plotter import create_plot
from tickets import get_lucky_tickets


def main():
    """точка входа
    """

    numbers = get_numbers()

    # рисуем диаграммы распределния номеров
    create_plot(numbers)

    # получаем счастливые билеты
    tickets = get_lucky_tickets(numbers)

    pprint(sorted(tickets.items(), key=lambda item: item[1], reverse=True))


if __name__ == '__main__':
    main()
