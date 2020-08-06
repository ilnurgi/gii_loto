"""хелперы
"""


def log(log_message: str):
    """простой логер работы
    :param log_message: тект сообщения
    """
    def wrapper(func):
        def inner(*args, **kwargs):
            formatted_log_message = log_message.format(**(kwargs or {}))
            print(f'-> START: {formatted_log_message}')
            result = func(*args, **kwargs)
            print(f'--> DONE: {formatted_log_message}')
            return result
        return inner
    return wrapper
