__lib__: str = "log95"
__version__: float = 1.2

from enum import Enum
from types import ModuleType
import datetime
from typing import LiteralString

try:
    import colorama # type: ignore
except ModuleNotFoundError:
    print("log95: colorama is not installed.")

class log95Levels(Enum):
    DEBUG = 0
    VERBOSE = 1
    CRITICAL_ERROR = 2
    ERROR = 3
    WARN = 4
    INFO = 5

class log95:
    def __init__(self, tag:str="...", level=log95Levels.CRITICAL_ERROR) -> None:
        self.tag = str(tag)
        self.level = int(level.value)
    def log(self, level: log95Levels, *args:str, seperator=" ") -> None:
        if level.value < self.level:
            return
        out = seperator.join(args)
        we_have_color = False
        for k,v in globals().items():
            if k == "colorama" and isinstance(v,ModuleType):
                we_have_color = True
                break
        def level_to_str(_level: log95Levels, _color: bool) -> LiteralString | str:
            match _level:
                # the same if theres color and when theres not
                    case log95Levels.DEBUG:
                        return f"DEBUG"
            if _color:
                match _level:
                    case log95Levels.VERBOSE:
                        return f"{colorama.Fore.LIGHTWHITE_EX}VERBOSE{colorama.Fore.RESET}" # type: ignore
                    case log95Levels.CRITICAL_ERROR:
                        return f"{colorama.Fore.RED}CRITICAL{colorama.Fore.RESET}" # type: ignore
                    case log95Levels.ERROR:
                        return f"{colorama.Fore.LIGHTRED_EX}ERROR{colorama.Fore.RESET}" # type: ignore
                    case log95Levels.WARN:
                        return f"{colorama.Fore.YELLOW}WARN{colorama.Fore.RESET}" # type: ignore
                    case log95Levels.INFO:
                        return f"{colorama.Fore.BLUE}INFO{colorama.Fore.RESET}" # type: ignore
            else:
                match _level:
                    case log95Levels.VERBOSE:
                        return f"VERBOSE"
                    case log95Levels.CRITICAL_ERROR:
                        return f"CRITICAL"
                    case log95Levels.ERROR:
                        return f"ERROR"
                    case log95Levels.WARN:
                        return f"WARN"
                    case log95Levels.INFO:
                        return f"INFO"
        print(f"[{self.tag}] ({level_to_str(level, we_have_color)}) @ ({datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S.%f')}) - {out}")
    def debug(self, *args:str, seperator=" ") -> None:
        self.log(log95Levels.DEBUG, *args, seperator)
    def verbose(self, *args:str, seperator=" ") -> None:
        self.log(log95Levels.VERBOSE, *args, seperator)
    def critical_error(self, *args:str, seperator=" ") -> None:
        self.log(log95Levels.CRITICAL_ERROR, *args, seperator)
    def error(self, *args:str, seperator=" ") -> None:
        self.log(log95Levels.ERROR, *args, seperator)
    def warning(self, *args:str, seperator=" ") -> None:
        self.log(log95Levels.WARN, *args, seperator)
    def info(self, *args:str, seperator=" ") -> None:
        self.log(log95Levels.INFO, *args, seperator)