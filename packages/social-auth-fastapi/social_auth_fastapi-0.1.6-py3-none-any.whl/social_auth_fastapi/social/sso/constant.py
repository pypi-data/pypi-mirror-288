from enum import Enum


class ProviderEnum(str, Enum):
    FACEBOOK: str = 'facebook'
    GITHUB: str = 'github'
    GOOGLE: str = 'google'
    FITBIT: str = 'fitbit'
    GITLAB: str = 'gitlab'
    LINE: str = 'line'
    LINKEDIN: str = 'linkedin'
    NOTION: str = 'notion'
    TWITTER: str = 'twitter'
