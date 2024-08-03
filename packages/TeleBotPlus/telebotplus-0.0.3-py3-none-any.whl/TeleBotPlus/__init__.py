"""
\u0420\u0430\u0437\u0440\u0430\u0431\u043E\u0442\u0447\u0438\u043A: MainPlay TG
https://t.me/MainPlayCh"""

__version_tuple__ = (0, 0, 3)
__depends__ = {
    "required": [
        "MainShortcuts",
        "requests",
        "telebot",
    ],
    "optional": [
        "aiohttp",
    ]
}
__scripts__ = []
__all__ = ["TeleBotPlus", "Assets"]
from .main import *
__all__.sort()
__version__ = "{}.{}.{}".format(*__version_tuple__)
