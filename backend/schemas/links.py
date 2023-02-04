
from dataclasses import dataclass
import re
from backend.core.config import env_config


class TelegramUsername(str):
    '''Telegram username validator.'''
    pattern = r"([A-Za-z0-9_]+)"

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not v:
            return v
        if len(v) > int(env_config.get('VITE_MAX_TELEGRAM_USERNAME_LENGTH')):
            raise ValueError('The Telegram username is too long.')
        match = re.match(cls.pattern, v)
        if not match:
            raise ValueError('Please enter a valid Telegram username.')
        return match.group(1)


class TelegramUsernameToUrl(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not v:
            return v
        return f"https://t.me/{v}"


class YoutubeChannelIDToUrl(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not v:
            return v
        return f"https://www.youtube.com/channel/{v}"


class YoutubeChannelID(str):
    '''YouTube channel ID validator.'''
    pattern = r"([A-Za-z0-9_\-]+)"

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not v:
            return v
        if len(v) > int(env_config.get('VITE_MAX_YOUTUBE_CHANNEL_ID_LENGTH')):
            raise ValueError('The YouTube channel ID is too long.')
        match = re.match(cls.pattern, v)
        if not match:
            raise ValueError('Please enter a valid YouTube channel ID.')
        return match.group(1)


class VKUsername(str):
    '''VKontakte username validator.'''
    pattern = r"([A-Za-z0-9_\.]+)"

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not v:
            return v
        if len(v) > int(env_config.get('VITE_MAX_VK_USERNAME_LENGTH')):
            raise ValueError('The VKontakte username is too long.')
        match = re.match(cls.pattern, v)
        if not match:
            raise ValueError('Please enter a valid VKontakte username.')
        return match.group(1)


class VKUsernameToUrl(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not v:
            return v
        return f"https://vk.com/{v}"
