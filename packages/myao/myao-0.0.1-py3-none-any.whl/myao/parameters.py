from dataclasses import dataclass
from enum import Enum
from typing import Dict, Set


class Subcategory(Enum):
    ANIME_MUSIC_VIDEO = 'Anime Music Video'              # Nyaa
    ENGLISH_TRANSLATED = 'English-translated'            # Nyaa
    NON_ENGLISH_TRANSLATED = 'Non-English-translated'    # Nyaa
    RAW = 'Raw'                                          # Nyaa
    LOSSLESS = 'Lossless'                                # Nyaa
    LOSSY = 'Lossy'                                      # Nyaa
    IDOL_PROMOTIONAL_VIDEO = 'Idol/Promotional Video'    # Nyaa
    GRAPHICS = 'Graphics'                                # Nyaa
    PHOTOS = 'Photos'                                    # Nyaa
    APPLICATIONS = 'Applications'                        # Nyaa
    GAMES = 'Games'                                      # Nyaa - Sukebei
    ANIME = 'Anime'                                      # Sukebei
    MANGA = 'Manga'                                      # Sukebei
    DOUJINSHI = 'Doujinshi'                              # Sukebei
    PICTURES = 'Pictures'                                # Sukebei
    PHOTOBOOKS_AND_PICTURES = 'Photobooks / Pictures'    # Sukebei
    VIDEOS = 'Videos'                                    # Sukebei


@dataclass
class _Category:
    name: str
    param: int
    subcategories: Dict[Subcategory, int]


class Category(Enum):
    ALL_CATEGORIES = _Category(name='All categories', param=0, subcategories={})

    # Nyaa
    ANIME = _Category(name='Anime', param=1, subcategories={
        Subcategory.ANIME_MUSIC_VIDEO: 1,
        Subcategory.ENGLISH_TRANSLATED: 2,
        Subcategory.NON_ENGLISH_TRANSLATED: 3,
        Subcategory.RAW: 4,
    })
    AUDIO = _Category(name="Audio", param=2, subcategories={
        Subcategory.LOSSLESS: 1,
        Subcategory.LOSSY: 2,
    })
    LITERATURE = _Category(name='Literature', param=3, subcategories={
        Subcategory.ENGLISH_TRANSLATED: 1,
        Subcategory.NON_ENGLISH_TRANSLATED: 2,
        Subcategory.RAW: 3,
    })
    LIVE_ACTION = _Category(name='Live Action', param=4, subcategories={
        Subcategory.ENGLISH_TRANSLATED: 1,
        Subcategory.IDOL_PROMOTIONAL_VIDEO: 2,
        Subcategory.NON_ENGLISH_TRANSLATED: 3,
        Subcategory.RAW: 4,
    })
    PICTURES = _Category(name='Pictures', param=5, subcategories={
        Subcategory.GRAPHICS: 1,
        Subcategory.PHOTOS: 2,
    })
    SOFTWARE = _Category(name='Software', param=6, subcategories={
        Subcategory.APPLICATIONS: 1,
        Subcategory.GAMES: 2,
    })

    # Sukebei
    ART = _Category(name='Art', param=1, subcategories={
        Subcategory.ANIME: 1,
        Subcategory.DOUJINSHI: 2,
        Subcategory.GAMES: 3,
        Subcategory.MANGA: 4,
        Subcategory.PICTURES: 5,
    })
    REAL_LIFE = _Category(name='Real Life', param=2, subcategories={
        Subcategory.PHOTOBOOKS_AND_PICTURES: 1,
        Subcategory.VIDEOS: 2,
    })

    @classmethod
    def get_category_by_name(cls, category_name: str) -> 'Category':
        return Category.__members__[category_name.upper().replace(' ', '_')]

    @classmethod
    def get_nyaa_categories(cls) -> Set['Category']:
        return {category for category in Category if category.is_nyaa_category()}

    @classmethod
    def get_subekei_categories(cls) -> Set['Category']:
        return {category for category in Category if category.is_sukebei_category()}

    def is_sukebei_category(self) -> bool:
        return self == Category.ALL_CATEGORIES or self in (Category.REAL_LIFE, Category.ART)

    def is_nyaa_category(self) -> bool:
        return self == Category.ALL_CATEGORIES or not self.is_sukebei_category()


class Sorting(Enum):
    SEEDERS = 'seeders'
    LEECHERS = 'leechers'
    ID = 'id'
    DOWNLOADS = 'downloads'
    COMMENTS = 'comments'


class Order(Enum):
    ASCENDING = 'asc'
    DESCENDANT = 'desc'


@dataclass
class _Filter:
    name: str
    param: int


class Filter(Enum):
    NO_FILTER = _Filter(name='No filter', param=0)
    NO_REMAKES = _Filter(name='No remakes', param=1)
    TRUSTED_ONLY = _Filter(name='Trusted only', param=2)


class TorrentType(Enum):
    REMAKE = "remake"
    TRUSTED = "trusted"
    DEFAULT = "default"
