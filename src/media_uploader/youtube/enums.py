from enum import Enum

__all__ = ["YoutubeCategory", "YoutubePrivacyStatus", "YoutubeLicense"]


class YoutubeCategory(Enum):
    FILM_ANIMATION = "1"
    AUTOS_VEHICLES = "2"
    MUSIC = "10"
    PETS_ANIMALS = "15"
    SPORTS = "17"
    SHORT_MOVIES = "18"
    TRAVEL_EVENTS = "19"
    GAMING = "20"
    VIDEOBLOGGING = "21"
    PEOPLE_BLOGS = "22"
    COMEDY = "23"
    ENTERTAINMENT = "24"
    NEWS_POLITICS = "25"
    HOWTO_STYLE = "26"
    EDUCATION = "27"
    SCIENCE_TECHNOLOGY = "28"
    NONPROFITS_ACTIVISM = "29"


class YoutubePrivacyStatus(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    UNLISTED = "unlisted"


class YoutubeLicense(Enum):
    YOUTUBE = "youtube"
    CREATIVE_COMMON = "creativeCommon"
