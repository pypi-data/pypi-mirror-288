from typing import Optional, Union
from myao.sites import Site, NyaaSite, SukebeiSite
from myao.errors import (
    InvalidCategory,
    InvalidSubcategory,
    InvalidPage
)
from myao.parameters import (
    Category,
    Subcategory,
    Filter,
    Order,
    Sorting
)


class Formatter:
    def __init__(self):
        self._site: Site = NyaaSite.NYAA_SI
        self._user: Optional[str] = None
        self._query = ''
        self._page = 0
        self._category = Category.ALL_CATEGORIES
        self._subcategory: Optional[Subcategory] = None
        self._sorting = Sorting.ID
        self._order = Order.DESCENDANT
        self._filter = Filter.NO_FILTER
        self._rss = False

    @property
    def site(self) -> Site:
        return self._site

    @site.setter
    def site(self, site: Site) -> None:
        if self._site != site:
            self._site = site
            self._category = Category.ALL_CATEGORIES
            self._subcategory = None

    @property
    def user(self) -> Optional[str]:
        return self._user

    @user.setter
    def user(self, user: str) -> None:
        self._user = user

    @property
    def query(self) -> Optional[str]:
        return self._query

    @query.setter
    def query(self, query: str = '') -> None:
        self._query = '+'.join(query.split())

    @property
    def page(self) -> int:
        return self._page

    @page.setter
    def page(self, page: int) -> None:
        if page < 0:
            raise InvalidPage(page)
        else:
            self._page = page

    @property
    def category(self) -> Category:
        return self._category

    @category.setter
    def category(self, category: Optional[Category]) -> None:
        if not category or category is Category.ALL_CATEGORIES:
            self._category = Category.ALL_CATEGORIES
            self._subcategory = None
        else:
            if self._category != category:
                if (
                    isinstance(self._site, NyaaSite) and category.is_sukebei_category()
                    or isinstance(self._site, SukebeiSite) and category.is_nyaa_category()
                ):
                    raise InvalidCategory(
                        f'Invalid category for site {self._site.value}: {category}'
                    )
                else:
                    self._category = category
                    self._subcategory = None

    @property
    def subcategory(self) -> Optional[Subcategory]:
        return self._subcategory

    @subcategory.setter
    def subcategory(self, subcategory: Optional[Subcategory]) -> None:
        if subcategory and subcategory not in self._category.value.subcategories:
            raise InvalidSubcategory(
                'Invalid subcategory for category '
                f'"{self._category.value.name}": {subcategory.name}'
            )
        self._subcategory = subcategory

    @property
    def sorting(self) -> Sorting:
        return self._sorting

    @sorting.setter
    def sorting(self, sorting: Optional[Sorting]) -> None:
        if not sorting:
            self._sorting = Sorting.ID
        else:
            self._sorting = sorting

    @property
    def order(self) -> Order:
        return self._order

    @order.setter
    def order(self, order: Optional[Order]) -> None:
        if not order:
            self._order = Order.DESCENDANT
        else:
            self._order = order

    @property
    def filter(self) -> Filter:
        return self._filter

    @filter.setter
    def filter(self, filter_: Optional[Filter]) -> None:
        if not filter_:
            self._filter = Filter.NO_FILTER
        else:
            self._filter = filter_

    @property
    def rss(self) -> bool:
        return self._rss

    @rss.setter
    def rss(self, rss: bool) -> None:
        self._rss = rss

    def format(self) -> str:
        return '{}/?q={}&p={}&c={}_{}&f={}&s={}&o={}&u={}&page={}'.format(
            self.site.value,
            self.query,
            self.page,
            self.category.value.param,
            self.category.value.subcategories[self.subcategory] if self.subcategory else 0,
            self.filter.value.param,
            self.sorting.value,
            self.order.value,
            self.user if self.user else '',
            'rss' if self.rss else ''
        )

    def get_download_torrent_url(self, code: Union[str, int]) -> str:
        return get_download_torrent_url(code, site=self.site)

    def get_single_torrent_url(self, code: Union[str, int]) -> str:
        return get_single_torrent_url(code, site=self.site)

    def get_user_url(self, user: str) -> str:
        return get_user_url(user, site=self.site, rss=self.rss)


def format_url(
    query='',
    *,
    user='',
    site: Site = NyaaSite.NYAA_SI,
    page=0,
    category: Optional[Category] = Category.ALL_CATEGORIES,
    subcategory: Optional[Subcategory] = None,
    filter_: Optional[Filter] = Filter.NO_FILTER,
    sorting: Optional[Sorting] = Sorting.ID,
    order: Optional[Order] = Order.DESCENDANT,
    rss=False,
) -> str:
    formatter = Formatter()
    formatter.query = query
    formatter.site = site
    formatter.user = user
    formatter.page = page
    formatter.category = category
    formatter.subcategory = subcategory
    formatter.filter = filter_
    formatter.sorting = sorting
    formatter.order = order
    formatter.rss = rss
    return formatter.format()


def get_download_torrent_url(code: Union[str, int], *, site: Site = NyaaSite.NYAA_SI) -> str:
    return f"{site.value}/download/{code}.torrent"


def get_single_torrent_url(code: Union[str, int], *, site: Site = NyaaSite.NYAA_SI) -> str:
    return f"{site.value}/view/{code}"


def get_user_url(user: str, *, site: Site = NyaaSite.NYAA_SI, rss=False) -> str:
    return f'{site.value}/?u={user}{"&page=rss" if rss else ""}'
