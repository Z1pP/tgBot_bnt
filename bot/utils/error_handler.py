from typing import Any, Callable, Coroutine
import functools

from aiogram.types import Message, CallbackQuery

from .logger import log_error


def error_handler(func: Callable[..., Coroutine[Any, Any, Any]]):
    """
    Декоратор для обработки ошибок в хэндлерах

    :param func: Асинхронная функция-обработчик
    :return: Обернутая функция с обработкой ошибок
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # Определяем источник вызова
            source = None
            for arg in args:
                if isinstance(arg, (Message, CallbackQuery)):
                    source = arg
                    break

            # Логируем полную трассировку
            log_error(f"Ошибка в {func.__name__}: {str(e)}", exc_info=True)

            # Отправляем уведомление об ошибке
            if source:
                bot = kwargs.get("bot") or args[0]
                if isinstance(source, Message):
                    await source.answer(
                        f"⚠️ Произошла ошибка: {str(e)}\n" "Администратор уже уведомлен."
                    )
                elif isinstance(source, CallbackQuery):
                    await source.message.answer(
                        f"⚠️ Произошла ошибка: {str(e)}\n" "Администратор уведомлен."
                    )
                    await source.answer()

            # Можно добавить отправку уведомления администратору
            # Например, через специальный сервис или прямое сообщение

            raise  # Пробрасываем исключение дальше

    return wrapper


def safe_execute(coro):
    """
    Безопасное выполнение корутины с логированием ошибок

    :param coro: Корутина для выполнения
    :return: Результат выполнения или None в случае ошибки
    """

    async def wrapper():
        try:
            return await coro
        except Exception as e:
            log_error(f"Ошибка при выполнении: {str(e)}", exc_info=True)
            return None

    return wrapper
