import os
import sys
import time
import difflib
import logging
import traceback
import threading
from enum import Enum
from typing import Union, Optional
from functools import total_ordering
from contextlib import contextmanager

__all__ = ['Verbosity', 'VerbosePrint', 'set_default_log_format']

text_color_map = {
    None: '',
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'bright black': '\033[30;1m',
    'bright red': '\033[31;1m',
    'bright green': '\033[32;1m',
    'bright yellow': '\033[33;1m',
    'bright blue': '\033[34;1m',
    'bright magenta': '\033[35;1m',
    'bright cyan': '\033[36;1m',
    'bright white': '\033[37;1m',    
    'darkred': '\033[91m',
    'reset': '\033[0m',
    'okgreen': '\033[92m'
}

def get_colored_text(text: str, color: str) -> str:
    """
    Returns the text formatted with the specified color.

    Parameters
    ----------
    text : str
        The text to be colored.
    color : str
        The color to apply to the text. 

    Returns
    -------
    str
        The input text with the specified color formatting.
    """
    return f"{text_color_map[color]}{text}{text_color_map['reset']}"

def format_comparison_text(text_left: str, text_right: str, 
                           equal_color: Optional[str] = None, 
                           delete_color: str = "red", 
                           insert_color: str = "green") -> tuple:
    """
    Formats two texts for comparison with color coding for differences.

    Parameters
    ----------
    text_left : str
        The left text to compare.
    text_right : str
        The right text to compare.
    equal_color : str, optional
        The color for equal text. Default is None.
    delete_color : str
        The color for deleted text. Default is 'red'.
    insert_color : str
        The color for inserted text. Default is 'green'.

    Returns
    -------
    tuple
        A tuple containing the formatted left and right texts.
    """
    codes = difflib.SequenceMatcher(a=text_left, b=text_right).get_opcodes()
    s_left = ""
    s_right = ""
    for code in codes:
        if code[0] == "equal":
            s = get_colored_text(text_left[code[1]:code[2]], equal_color)
            s_left += s
            s_right += s
        elif code[0] == "delete":
            s_left += get_colored_text(text_left[code[1]:code[2]], delete_color)
        elif code[0] == "insert":
            s_right += get_colored_text(text_right[code[3]:code[4]], insert_color)
        elif code[0] == "replace":
            s_left += get_colored_text(text_left[code[1]:code[2]], delete_color)
            s_right += get_colored_text(text_right[code[3]:code[4]], insert_color)
    return s_left, s_right

getThreads = True
getMultiprocessing = True
getProcesses = True

@total_ordering
class Verbosity(Enum):
    """
    Enum for verbosity levels.

    Attributes
    ----------
    SILENT : Verbosity
        No output.
    CRITICAL : Verbosity
        Critical errors.
    ERROR : Verbosity
        Errors.
    TIPS : Verbosity
        Tips.
    WARNING : Verbosity
        Warnings.
    INFO : Verbosity
        Information.
    DEBUG : Verbosity
        Debugging information.
    IGNORE : Verbosity
        Ignore messages.
    """
    SILENT = (100, 'SILENT')
    CRITICAL = (50, 'CRITICAL')
    ERROR = (40, 'ERROR')
    TIPS = (35, 'TIPS')
    WARNING = (30, 'WARNING')
    INFO = (20, 'INFO')
    DEBUG = (10, 'DEBUG')
    IGNORE = (0, 'IGNORE')
    
    def __new__(cls, value: int, levelname: str = ""):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.levelname = levelname
        return obj    
    
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        elif isinstance(other, int):
            return self.value < other
        elif isinstance(other, str):
            return self.value < getattr(self, other.upper()).value
        return NotImplemented
    
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        elif isinstance(other, str):
            return self.value == getattr(self, other.upper()).value
        return NotImplemented
        
class VerbosePrint:
    """
    A class for managing verbose printing.

    Parameters
    ----------
    verbosity : Union[int, Verbosity, str], optional
        The verbosity level. Default is Verbosity.INFO.
    fmt : str, optional
        The format string for messages. Default is None.
    name : str, optional
        The name for the logger. Default is ''.
    msecfmt : str, optional
        The format string for milliseconds. Default is None.
    datefmt : str, optional
        The date format string. Default is None.

    Methods
    -------
    silent(text='', color=None, bare=False)
        Silent print (no output).
    tips(text='', color=None, bare=False)
        Print tips.
    info(text='', color=None, bare=False)
        Print information.
    warning(text='', color=None, bare=False)
        Print warnings.
    error(text='', color=None, bare=False)
        Print errors.
    critical(text='', color=None, bare=False)
        Print critical errors.
    debug(text='', color=None, bare=False)
        Print debug information.
    write(text='', color=None)
        Write text with no formatting.
    set_format(fmt=None)
        Set the message format.
    set_timefmt(datefmt=None, msecfmt=None)
        Set the time format.
    format_time()
        Format the current time.
    """
    
    FORMATS = {
        'basic': '[%(levelname)s] %(message)s',
        'detailed': '%(asctime)s | PID:%(process)d, TID:%(threadName)s | %(levelname)s | %(message)s'
    }
    DEFAULT_FORMAT = FORMATS['basic']
    DEFAULT_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
    DEFAULT_MSECFORMAT = '%s.%03d'
    ASCTIME_SEARCH = '%(asctime)'
    
    @property
    def verbosity(self):
        return self._verbosity
    
    @verbosity.setter
    def verbosity(self, val):
        if isinstance(val, str):
            try:
                v = getattr(Verbosity, val.upper())
            except Exception:
                raise ValueError(f"invalid verbosity level: {val}")
            self._verbosity = v
        else:
            self._verbosity = val

    def __init__(self, verbosity: Union[int, Verbosity, str] = Verbosity.INFO,
                 fmt: Optional[str] = None, name: Optional[str] = '',
                 msecfmt: Optional[str] = None,
                 datefmt: Optional[str] = None):
        self.verbosity = verbosity
        self.set_format(fmt)
        self.set_timefmt(datefmt, msecfmt)
        self._name = name
        
    def silent(self, text: str = '', color: Optional[str] = None, bare: bool = False):
        pass
        
    def tips(self, text: str = '', color: Optional[str] = None, bare: bool = False):
        self.__call__(text, Verbosity.TIPS, color=color, bare=bare)
        
    def info(self, text: str = '', color: Optional[str] = None, bare: bool = False):
        self.__call__(text, Verbosity.INFO, color=color, bare=bare)
        
    def warning(self, text: str = '', color: Optional[str] = None, bare: bool = False):
        self.__call__(text, Verbosity.WARNING, color=color, bare=bare)
        
    def error(self, text: str = '', color: Optional[str] = None, bare: bool = False):
        self.__call__(text, Verbosity.ERROR, color=color, bare=bare)
        
    def critical(self, text: str = '', color: Optional[str] = None, bare: bool = False):
        self.__call__(text, Verbosity.CRITICAL, color=color, bare=bare)

    def debug(self, text: str = '', color: Optional[str] = None, bare: bool = False):
        self.__call__(text, Verbosity.DEBUG, color=color, bare=bare)

    def write(self, text: str = '', color: Optional[str] = None):
        self.__call__(text, Verbosity.SILENT, color=color, bare=True)
        
    def set_format(self, fmt: Optional[str] = None):
        """
        Set the message format.

        Parameters
        ----------
        fmt : str, optional
            The format string for messages. Default is None.
        """
        if fmt is None:
            fmt = self.DEFAULT_FORMAT
        elif fmt in self.FORMATS:
            fmt = self.FORMATS[fmt]
        self._formatter = logging.Formatter(fmt)
        
    def set_timefmt(self, datefmt: Optional[str] = None, msecfmt: Optional[str] = None):
        """
        Set the time format.

        Parameters
        ----------
        datefmt : str, optional
            The date format string. Default is None.
        msecfmt : str, optional
            The format string for milliseconds. Default is None.
        """
        if datefmt is None:
            datefmt = self.DEFAULT_DATEFORMAT
        if msecfmt is None:
            msecfmt = self.DEFAULT_MSECFORMAT
        self._datefmt = datefmt
        self._msecfmt = msecfmt
        
    def format_time(self) -> str:
        """
        Format the current time.

        Returns
        -------
        str
            The formatted current time string.
        """
        _ct = time.time()
        ct = self._formatter.converter(_ct)
        s = time.strftime(self._datefmt, ct)
        if self._msecfmt:
            msecs = int((_ct - int(_ct)) * 1000) + 0.0
            s = self._msecfmt % (s, msecs)
        return s
        
    def __call__(self, text: str, verbosity: Union[int, Verbosity] = Verbosity.INFO,
                 color: Optional[str] = None, bare: bool = False):
        """
        Print the text with the specified verbosity level and color.

        Parameters
        ----------
        text : str
            The text to print.
        verbosity : Union[int, Verbosity], optional
            The verbosity level. Default is Verbosity.INFO.
        color : str, optional
            The color to apply to the text. Default is None.
        bare : bool, optional
            If True, prints text without formatting. Default is False.
        """
        if verbosity < self.verbosity:
            return None
        if color:
            text = f"{text_color_map[color]}{text}{text_color_map['reset']}"
        if not bare:
            if hasattr(verbosity, 'levelname'):
                levelname = verbosity.levelname
            else:
                levelname = f"Level {verbosity}"
            if self._formatter.usesTime():
                asctime = self.format_time()
            else:
                asctime = None
            if getThreads:
                thread = threading.get_ident()
                threadName = threading.current_thread().name
            else:
                thread = None
                threadName = None
            if getProcesses and hasattr(os, 'getpid'):
                process = os.getpid()
            else:
                process = None
            args = {
                'name': self._name,
                'message': text,
                'levelname': levelname,
                'asctime': asctime,
                'thread': thread,
                'threadName': threadName,
                'process': process
            }
            text = self._formatter._fmt % args
        sys.stdout.write(f"{text}\n")
        
@contextmanager
def switch_verbosity(target: VerbosePrint, verbosity: Union[int, str]):
    """
    Context manager to switch verbosity temporarily.

    Parameters
    ----------
    target : VerbosePrint
        The target VerbosePrint instance.
    verbosity : Union[int, str]
        The new verbosity level to set temporarily.

    Yields
    ------
    None
    """
    try:
        orig_verbosity = target.verbosity
        target.verbosity = verbosity
        yield
    except Exception:
        traceback.print_exc(file=sys.stdout)
    finally:
        target.verbosity = orig_verbosity

def set_default_log_format(fmt:str='basic'):
    if fmt in VerbosePrint.FORMATS:
        fmt = VerbosePrint.FORMATS[fmt]
    VerbosePrint.DEFAULT_FORMAT = fmt