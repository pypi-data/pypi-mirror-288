import logging
from enum import Enum
from datetime import datetime
from typing import Callable, List, Union
from bs4 import BeautifulSoup
from myao.containers import Comment, Torrent, User, View
from myao.parameters import Category, Subcategory, TorrentType
from myao.errors import NoResultsFound, UnexpectedError
from myao.magnets import magnet_builder
from myao.utils import convert_to_bytes


logger = logging.getLogger(__name__)


class Parser(Enum):
    HTML = "html.parser"
    LXML = "lxml"
    HTML5LIB = "html5lib"


class Extractor:
    def __init__(self, parser: Parser = Parser.HTML):
        self.parser = parser

    def get_multiple_torrents(self, content: Union[str, bytes]) -> List[Torrent]:
        return get_multiple_torrents(content, self.parser)

    def get_multiple_torrents_rss(self, content: Union[str, bytes]) -> List[Torrent]:
        return get_multiple_torrents_rss(content, self.parser)

    def get_view(self, content: Union[str, bytes]) -> View:
        return get_view(content, self.parser)

    def get_single_torrent(self, content: Union[str, bytes]) -> Torrent:
        return get_single_torrent(content, self.parser)

    def get_comments(self, content: Union[str, bytes]) -> List[Comment]:
        return get_comments(content, self.parser)

    def get_description(self, content: Union[str, bytes]) -> str:
        return get_description(content, self.parser)


def _log_unexpected_errors(func: Callable) -> Callable:
    def _inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoResultsFound as e:
            raise e
        except Exception as e:
            msg = f"Please provide this log error to https://github.com/g3nsy/myao/issues"
            logger.error(e)
            logger.error(msg)
            raise UnexpectedError(e, msg)
    return _inner


@_log_unexpected_errors
def get_multiple_torrents(content: Union[str, bytes], parser=Parser.HTML) -> List[Torrent]:
    soup = BeautifulSoup(content, parser.value)
    tbody_entries = soup.find('tbody')
    if not tbody_entries:
        raise NoResultsFound
    torrents: List[Torrent] = []
    for entry in tbody_entries.find_all('tr'):  # type: ignore

        cols = entry.find_all('td')
        col0 = cols[0].find_all('a')
        col1 = cols[1].find_all('a')
        col2 = cols[2].find_all('a')

        category_name, subcategory_name = col0[0]['title'].split(' - ')
        category = Category.get_category_by_name(category_name)
        subcategory = Subcategory(subcategory_name)

        class_value = entry.get('class')
        torrent_type = (
            TorrentType.TRUSTED if class_value == "success"
            else TorrentType.REMAKE if class_value == "danger"
            else TorrentType.DEFAULT
        )

        if len(col1) == 2:
            title = col1[1]['title']
            comments = int(col1[0]['title'].split()[0])
        else:
            title = col1[0]['title']
            comments = 0

        seeders = int(cols[5].get_text())
        leechers = int(cols[6].get_text())
        completed_downloads = int(cols[7].get_text())
        date = datetime.strptime(cols[4].get_text(), '%Y-%m-%d %H:%M')
        size = convert_to_bytes(cols[3].get_text())
        magnet_link = col2[1]['href']
        code = int(col2[0]['href'][10:-8])

        torrents.append(
            Torrent(
                title=title,
                category=category,
                subcategory=subcategory,
                seeders=seeders,
                leechers=leechers,
                comments=comments,
                completed_downloads=completed_downloads,
                date=date,
                size=size,
                torrent_type=torrent_type,
                magnet_link=magnet_link,
                code=code,
            )
        )
    return torrents


@_log_unexpected_errors
def get_multiple_torrents_rss(content: Union[str, bytes], parser=Parser.HTML) -> List[Torrent]:
    soup = BeautifulSoup(content, parser.value)
    torrents: List[Torrent] = []
    items = soup.find_all('item')
    if not items:
        raise NoResultsFound
    for item in items:
        category_name, subcategory_name = item.find('nyaa:category').get_text().split(' - ')
        category = Category.get_category_by_name(category_name.strip())
        subcategory = Subcategory(subcategory_name.strip())

        is_trusted = item.find('nyaa:trusted') == 'Yes'
        is_remake = item.find('nyaa:remake') == 'Yes'

        torrent_type = (
            TorrentType.TRUSTED if is_trusted
            else TorrentType.REMAKE if is_remake
            else TorrentType.DEFAULT
        )

        title = item.title.text
        info_hash = item.find('nyaa:infohash').text
        seeders = int(item.find('nyaa:seeders').text)
        leechers = int(item.find('nyaa:leechers').text)
        comments = int(item.find('nyaa:comments').text)
        completed_downloads = int(item.find('nyaa:downloads').text)
        date = datetime.strptime(item.find('pubdate').text, '%a, %d %b %Y %H:%M:%S %z')
        size = convert_to_bytes(item.find('nyaa:size').text)
        code = int(item.find('guid').get_text().split('/')[-1])
        magnet_link = magnet_builder(info_hash, title)

        torrents.append(
            Torrent(
                title=title,
                category=category,
                subcategory=subcategory,
                seeders=seeders,
                leechers=leechers,
                comments=comments,
                completed_downloads=completed_downloads,
                date=date,
                size=size,
                torrent_type=torrent_type,
                info_hash=info_hash,
                magnet_link=magnet_link,
                code=code,
            )
        )
    return torrents


@_log_unexpected_errors
def get_view(content: Union[str, bytes], parser=Parser.HTML) -> View:
    soup = BeautifulSoup(content, parser.value)
    torrent = _get_single_torrent(soup)
    comments = _get_comments(soup)
    description = _get_description(soup)
    return View(
        torrent=torrent,
        description=description,
        comments=comments
    )


@_log_unexpected_errors
def get_description(content: Union[str, bytes], parser=Parser.HTML) -> str:
    return _get_description(BeautifulSoup(content, parser.value))


def _get_description(soup: BeautifulSoup) -> str:
    return soup.find('div', {'id': 'torrent-description'}).get_text()  # type: ignore


@_log_unexpected_errors
def get_comments(content: Union[str, bytes], parser=Parser.HTML) -> List[Comment]:
    return _get_comments(BeautifulSoup(content, parser.value))


def _get_comments(soup: BeautifulSoup) -> List[Comment]:
    comments_data = soup.find('div', {'id': 'comments'})
    comment_class = {'class': 'panel panel-default comment-panel'}
    comments: List[Comment] = []
    for comment_data in comments_data.find_all('div', comment_class):  # type: ignore
        try:
            user = User(
                name=comment_data.find('a', {'class': 'text-default'}).get_text(),
                trusted=False
            )
        except AttributeError:
            user = User(
                name=comment_data.find('a', {'class': 'text-success'}).get_text(),
                trusted=True
            )

        date = comment_data.find('small').get_text()
        text = comment_data.find('div', {'class': 'comment-content'}).get_text()

        avatar = comment_data.find('img')['src']
        if avatar.startswith('/'):
            avatar = None

        comments.append(Comment(
            user=user,
            avatar=avatar,
            date=date,
            text=text
        ))

    return comments


@_log_unexpected_errors
def get_single_torrent(content: Union[str, bytes], parser=Parser.HTML) -> Torrent:
    return _get_single_torrent(BeautifulSoup(content, parser.value))


def _get_single_torrent(soup: BeautifulSoup) -> Torrent:
    title = soup.find('h3', {'class': 'panel-title'}).get_text(strip=True)  # type: ignore
    panel_body = soup.find('div', {'class': 'panel-body'})
    rows = panel_body.find_all('div', {'class': 'row'})  # type: ignore

    comments_data = soup.find(
        'div', {'id': 'comments'}
    ).find('h3', {'class': 'panel-title'})  # type: ignore
    comments = int(comments_data.get_text().split(' - ')[1])  # type: ignore

    div_row_0 = rows[0].find_all('div')
    div_row_1 = rows[1].find_all('div')
    div_row_2 = rows[2].find_all('div')
    div_row_3 = rows[3].find_all('div')
    div_row_4 = rows[4].find_all('div')

    category_name, subcategory_name = div_row_0[1].get_text().split(' - ')
    category = Category.get_category_by_name(category_name.strip())
    subcategory = Subcategory(subcategory_name.strip())

    date = datetime.strptime(div_row_0[3].get_text(strip=True), '%Y-%m-%d %H:%M %Z')

    try:
        trusted = div_row_1[1].find('a')['title'] == 'Trusted'
    except TypeError:  # Anonymous
        trusted = False

    name = div_row_1[1].get_text(strip=True)
    submitter = User(name=name, trusted=trusted)
    seeders = int(div_row_1[3].get_text())
    information = div_row_2[1].get_text()
    leechers = int(div_row_2[3].get_text())
    size = convert_to_bytes(div_row_3[1].get_text())
    completed_downloads = int(div_row_3[3].get_text())
    info_hash = div_row_4[1].get_text()
    footer_attrs = soup.find(
        'div', {'class': 'panel-footer clearfix'}
    ).find_all('a')  # type: ignore
    code = int(footer_attrs[0]['href'][10:-8])
    magnet_link = footer_attrs[1]['href']
    information = information if information != 'No information.' else None

    return Torrent(
        size=size,
        date=date,
        category=category,
        subcategory=subcategory,
        submitter=submitter,
        completed_downloads=completed_downloads,
        code=code,
        magnet_link=magnet_link,
        seeders=seeders,
        leechers=leechers,
        title=title,
        information=information,
        info_hash=info_hash,
        comments=comments
    )
