from .containers import (
    Torrent,
    Comment,
    View,
    User
)

from .sites import (
    Site,
    NyaaSite,
    SukebeiSite
)

from .extractors import (
    Extractor,
    Parser,
    get_multiple_torrents,
    get_multiple_torrents_rss,
    get_single_torrent,
    get_description,
    get_comments,
    get_view
)

from .parameters import (
    Category,
    Subcategory,
    Order,
    Sorting,
    Filter
)

from .errors import (
    MyaoError,
    FormatterError,
    InvalidCategory,
    InvalidPage,
    InvalidSubcategory,
    ExtractionError,
    NoResultsFound,
)

from .urls import (
    Formatter,
    format_url,
    get_user_url,
    get_single_torrent_url,
    get_download_torrent_url,
)

from .magnets import magnet_builder


__all__ = [
    # Containers
    'Torrent',
    'Comment',
    'Comment',
    'View',
    'User',

    # Extractors
    'Extractor',
    'Parser',
    'get_multiple_torrents',
    'get_multiple_torrents_rss',
    'get_single_torrent',
    'get_description',
    'get_comments',
    'get_view',

    # Sites
    'Site',
    'NyaaSite',
    'SukebeiSite',

    # Parameters
    'Category',
    'Subcategory',
    'Order',
    'Sorting',
    'Filter',

    # Urls
    'Formatter',
    'format_url',
    'get_user_url',
    'get_single_torrent_url',
    'get_download_torrent_url',

    # Errors
    'MyaoError',
    'FormatterError',
    'InvalidCategory',
    'InvalidSubcategory',
    'InvalidPage',
    'ExtractionError',
    'NoResultsFound',

    # Magnet
    'magnet_builder'
]


__version__ = "0.0.1"
