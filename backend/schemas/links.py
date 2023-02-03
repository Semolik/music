from pydantic import BaseModel, validator, HttpUrl
import re
from fastapi import Query

from pydantic import BaseModel, validator, HttpUrl, conint, root_validator
import re


class TelegramURL(HttpUrl):
    '''Telegram URL validator.'''
    pattern = r"https?://(t\.me|telegram\.me)/([A-Za-z0-9_]+)"

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        match = re.match(cls.pattern, v)
        if not match:
            raise ValueError('Please enter a valid Telegram URL.')
        return match.group(2)


class YouTubeURL(HttpUrl):
    '''YouTube URL validator.'''
    pattern = r"(https?://www\.youtube\.com/channel/[A-Za-z0-9_\-]+|https?://www\.youtube\.com/c/[A-Za-z0-9_\-]+|https?://youtube\.com/channel/[A-Za-z0-9_\-]+|https?://youtube\.com/c/[A-Za-z0-9_\-]+)"

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        match = re.match(cls.pattern, v)
        if not match:
            raise ValueError('Please enter a valid YouTube channel URL.')
        if match.lastindex is None or match.lastindex < 5:
            raise ValueError('The YouTube channel URL is not valid.')
        return match.group(2) or match.group(3) or match.group(4) or match.group(5)


class VKProfileURL(HttpUrl):
    '''VKontakte URL validator.'''
    pattern = r"https://vk\.com/([A-Za-z0-9_\.]+)"

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        match = re.match(cls.pattern, v)
        if not match:
            raise ValueError('Please enter a valid VKontakte URL.')
        return match.group(1)
