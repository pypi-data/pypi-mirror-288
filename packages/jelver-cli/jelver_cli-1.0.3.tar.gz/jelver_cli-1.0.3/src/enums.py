""" File to house Enums """

from enum import Enum


class BrowserType(Enum):
    """
    Enum for browsers
    """
    CHROMIUM = 'CHROMIUM'
    FIREFOX = 'FIREFOX'
    WEBKIT = 'WEBKIT'
    SAFARI = 'SAFARI'
    EDGE = 'EDGE'


class CaseType(Enum):
    """
    Class to house different CaseTypes
    """
    ROUTE = 'ROUTE'
