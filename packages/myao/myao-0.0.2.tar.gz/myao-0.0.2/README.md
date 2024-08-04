# Myao
## A flexible Nyaa API written in Python.
![Version](https://img.shields.io/badge/version-0.0.2-blue)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://en.wikipedia.org/wiki/MIT_License)
---
This library is intended to allow users to interact with Nyaa and Sukebei 
without forcing the use of a specific HTTP library like requests and the 
use of a specific HTML parser like lxml. Only static components are 
implemented: a component for defining URLs and for extracting and organizing 
the resulting data.

## Installation
```shell
pip install myao
```

## Usage
More examples in the 'examples' directory
```python
import requests

from myao.urls import get_single_torrent_url, format_url
from myao.parameters import Category, Subcategory, Filter, Order
from myao.extractors import (
    get_comments,
    get_multiple_torrents,
    get_multiple_torrents_rss,
    Parser
)


# ---------- Comments ----------------- #

code = 1273100
url = get_single_torrent_url(code)

response = requests.get(url)
response.raise_for_status()

comments = get_comments(
    content=response.content, 
    parser=Parser.LXML
)

# ----------- Torrents ---------------- #

url = format_url(
    query='Lain',
    category=Category.ANIME,
    subcategory=Subcategory.ENGLISH_TRANSLATED,
    filter_=Filter.TRUSTED_ONLY,
    order=Order.ASCENDING
)

response = requests.get(url)
response.raise_for_status()

torrents = get_multiple_torrents(
    content=response.content, 
    parser=Parser.HTML
)

# ----------- Torrents RSS ------------ #

url = format_url(
    query='Steins;Gate',
    category=Category.LITERATURE,
    subcategory=Subcategory.RAW,
    rss=True
)

response = requests.get(url)
response.raise_for_status()

torrents = get_multiple_torrents_rss(
    content=response.content,
    parser=Parser.HTML5LIB
)
```
