"""рисовальщик графиков
"""

import os

from matplotlib import pyplot

from gii_loto import settings


def __create_plot(ax, numbers: dict, editions: tuple, label_x: str):
    """создаем график
    :param ax: где рисуем
    :param numbers: данные по цифрам
    :param editions: указанные тиражи
    :param label_x: подпись для оси Х
    """
    miss_counter = {}
    for edition in editions:
        edition_numbers = numbers[edition]
        for edition_number in edition_numbers:
            miss_counter.setdefault(edition_number, 0)
            miss_counter[edition_number] += 1
    x = []
    y = []
    for number, count in sorted(miss_counter.items()):
        x.append(number)
        y.append(count)
    ax.scatter(x, y)

    for number, counter in miss_counter.items():
        ax.text(number, counter, f'{number}')

    ax.set_xlabel(label_x)


def create_plot(numbers):
    """отрисовка графиков
    :param numbers: сведения по числам
    """
    rows = 2
    columns = 5
    fig, axs = pyplot.subplots(rows, columns, figsize=(25.6, 10.8))

    plots = (
        (settings.EDITIONS[-10:], 'last 10'),
        (settings.EDITIONS[-20:], 'last 20'),
        (settings.EDITIONS[-30:], 'last 30'),
        (settings.EDITIONS[-40:], 'last 40'),
        (settings.EDITIONS[-50:], 'last 50'),
        (settings.EDITIONS[-100:], 'last 100'),
        (settings.EDITIONS[-200:], 'last 200'),
        (settings.EDITIONS[-300:], 'last 300'),
        (settings.EDITIONS[-400:], 'last 400'),
        (settings.EDITIONS, f'last {settings.EDITIONS_COUNT}'),
    )
    plot_index = 0
    for row in range(rows):
        for col in range(columns):
            plot_editions, text = plots[plot_index]
            plot_index += 1
            __create_plot(axs[row, col], numbers, plot_editions, text)

    fig.tight_layout()
    fig.savefig(os.path.join(settings.SETTINGS_DIR, 'plot.png'))
