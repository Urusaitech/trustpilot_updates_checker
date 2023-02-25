import asyncio
import sys
import os
from asyncio.proactor_events import _ProactorBasePipeTransport
from functools import wraps
import platform
from typing import TypeVar, Callable
from configs import token, chat_id
from aiogram import Bot


async def send_notice() -> None:
    # bot = Bot(token=os.environ["BOT_TOKEN"])
    bot = Bot(token=token)
    await bot.send_message(chat_id, "reviews update detected")


T = TypeVar("T")


def silence_event_loop_closed(func) -> Callable[[T], T]:
    """
    checks if the correct error was silences
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != "Event loop is closed":
                raise

    return wrapper


def main() -> None:
    """
    This funcs checks if it runs on Windows to silence an exception in send_message(),
    also it sets os looping policy
    :return:
    """
    if platform.system() == "Windows":
        # Silence the exception here.
        _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(
            _ProactorBasePipeTransport.__del__
        )

    if (
        sys.version_info[0] == 3
        and sys.version_info[1] >= 8
        and sys.platform.startswith("win")
    ):
        # set Loop policy
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(send_notice())


if __name__ == "__main__":
    main()
