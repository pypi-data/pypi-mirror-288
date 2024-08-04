# coding: utf-8
"""
    ShaarPy :: Tools

    - Importing/Exporting in Netscape HTML File
    - Load article from url with image/video
    - Manage Markdown file creation
"""
import base64
import copy
from datetime import datetime
import html
import logging
import os
from pathlib import Path
import re
from typing import NoReturn
from urllib.parse import urlparse
from slugify import slugify

from bs4 import BeautifulSoup
from django.utils import timezone
from django.utils.text import Truncator
from jinja2 import Environment, PackageLoader
from newspaper import Article

import newspaper
import pypandoc
from rich.console import Console
from rich.table import Table
from shaarpy.models import Links
from shaarpy import settings

console = Console()
logger = logging.getLogger('tools')
"""
    URL
"""


def url_cleaning(url: str) -> str:
    """
    drop unexpected content of the URL from the bookmarklet

    param url: url of the website
    :return string url
    """

    if url:
        for pattern in ('&utm_source=', '?utm_source=', '&utm_medium=', '#xtor=RSS-'):
            pos = url.find(pattern)
            if pos > 0:
                url = url[0:pos]
    return url


# ARTICLES MANAGEMENT


def _get_host(url: str) -> str:
    """
    go to get the schema and hostname and port related to the given url

    param url: url of the website
    :return string 'hostname'
    """

    o = urlparse(url)
    hostname = o.scheme + '://' + o.hostname
    port = ''
    if o.port is not None and o.port != 80:
        port = ':' + str(o.port)
    hostname += port
    return hostname


def _get_brand(url: str) -> str:
    """
    go to get the brand name related to the given url

    url: url of the website
    :return string of the Brand
    """
    brand = newspaper.build(url=_get_host(url))
    brand.download()
    brand.parse()
    return brand.brand


def drop_image_node(content: str) -> tuple:
    """
    drop the image node if found

    content: content of the html possibly containing the img
    return the first found image and the content
    """
    my_image = ''
    soup = BeautifulSoup(content, 'html.parser')
    if soup.find_all('img', src=True):
        image = soup.find_all('img', src=True)[0]
        my_image = copy.copy(image['src'])
        # if not using copy.copy(image) before
        # image.decompose(), it drops content of the 2 vars
        # image and my_image
        image.decompose()
    return my_image, soup


def grab_full_article(url: str) -> tuple:
    """
        get the complete article page from the URL
    url: URL of the article to get
    return title text image video or the URL in case of ArticleException
    """
    # get the complete article
    r = Article(url, keep_article_html=True)
    try:
        r.download()
        r.parse()
        article_html = r.article_html
        video = r.movies[0] if len(r.movies) > 0 else ''
        image = ''
        # check if there is a top_image
        if r.top_image:
            # go to check image in the article_html and grab the first one found in article_html
            # it may happened that top_image is not the same in the content of article_html
            # so go pickup this one and remove it in the the content of article_html
            image, article_html = drop_image_node(article_html)
        # convert into markdown
        output = Truncator(article_html).chars("400", html=True)
        text = pypandoc.convert_text(output, 'md', format='html')
        title = r.title + ' - ' + _get_brand(url)

        return title, text, image, video
    except newspaper.article.ArticleException:
        return url, "", "", ""


# MARKDOWN MANAGEMENT


def rm_md_file(title: str) -> NoReturn:
    """
        rm a markdown file
    title: the name of the file to remove
    """
    file_name = slugify(title) + '.md'
    file_md = f'{settings.SHAARPY_LOCALSTORAGE_MD}/{file_name}'
    if os.path.exists(file_md):
        os.remove(file_md)


def create_md_file(storage: str, title: str, url: str, text: str,
                   tags: str, date_created: str, private: bool, image: str, video: str) -> NoReturn:
    """
        create a markdown file
    storage: path of the folder where to store the file
    title: title of the file
    url: url of the article
    text: text of the article
    tags: tags if provided
    date_created: creation date
    private: boolean true/false
    image: the main image if any
    video: the main video if any
    """

    data = {'title': title,
            'url': url,
            'text': text,
            'date': date_created,
            'private': private,
            'tags': tags,
            'image': image,
            'video': video,
            'author': settings.SHAARPY_AUTHOR,
            'style': settings.SHAARPY_STYLE}

    env = Environment(
        loader=PackageLoader('shaarpy', 'templates'), autoescape=True
    )
    template = env.get_template('shaarpy/shaarpy_markdown.md')
    output = template.render(data=data)
    file_name = slugify(title) + '.md'
    file_md = f'{storage}/{file_name}'
    # overwrite existing file with same slug name
    with open(file_md, 'w') as ls:
        ls.write(output)


# CRC Stuff


def crc_that(string: str) -> int:
    """
    the PHP's hash(crc32) in Python :P

    implem in python:
       https://chezsoi.org/shaarli/shaare/U7admg
       https://stackoverflow.com/a/50843127/636849
    """
    a = bytearray(string, "utf-8")
    crc = 0xffffffff
    for x in a:
        crc ^= x << 24
        for k in range(8):
            crc = (crc << 1) ^ 0x04c11db7 if crc & 0x80000000 else crc << 1
    crc = ~crc
    crc &= 0xffffffff
    return int.from_bytes(crc.to_bytes(4, 'big'), 'little')


def small_hash(text: str) -> str:
    """
    Returns the small hash of a string, using RFC 4648 base64url format
   eg. smallHash('20111006_131924') --> yZH23w
   Small hashes:
     - are unique (well, as unique as crc32, at last)
     - are always 6 characters long.
     - only use the following characters: a-z A-Z 0-9 - _ @
     - are NOT cryptographically secure (they CAN be forged)
    In Shaarli, they are used as a tinyurl-like link to individual entries.
    """
    number = crc_that(text)

    number_bytes = number.to_bytes((number.bit_length() + 7) // 8, byteorder='big')

    encoded = base64.b64encode(number_bytes)
    final_value = encoded.decode().rstrip('=').replace('+', '-').replace('/', '_')
    return final_value


# IMPORTING SHAARLI FILE

def import_shaarli(the_file: str, reload_article_from_url: str) -> NoReturn:  # noqa: C901
    """
    the_file: name of the file to import
    reload_article_from_url: article url
    """
    private = 0
    with open(the_file, 'r') as f:
        data = f.read()
        msg = f"ShaarPy :: importing {the_file}"
        logger.debug(msg)

    if data.startswith('<!DOCTYPE NETSCAPE-Bookmark-file-1>'):
        i = 0
        table = Table(show_header=True, header_style="bold magenta")

        table.add_column("Title", style="cyan")
        table.add_column("Private", style="yellow")
        table.add_column("Date", style="dim")

        for html_article in data.split('<DT>'):
            i += 1
            link = {'url': '',
                    'title': '',
                    'text': '',
                    'tags': '',
                    'image': None,
                    'video': None,
                    'date_created': '',
                    'private': False}
            if i == 1:
                continue

            if len(html_article.split('<DD>')) == 2:
                line, text = html_article.split('<DD>')
                link['text'] = html.unescape(text)

            for line in html_article.split('<DD>'):
                if line.startswith('<A '):
                    matches = re.match(r"<A (.*?)>(.*?)</A>", line)

                    attrs = matches[1]

                    link['title'] = matches[2] if matches[2] else ''
                    link['title'] = html.unescape(link['title'])

                    for attr in attrs.split(" "):
                        matches = re.match(r'([A-Z_]+)="(.+)"', attr)
                        attr_found = matches[1]
                        value_found = matches[2]
                        if attr_found == 'HREF':
                            link['url'] = html.unescape(value_found)
                        elif attr_found == 'ADD_DATE':
                            raw_add_date = int(value_found)
                            if raw_add_date > 30000000000:
                                raw_add_date /= 1000
                            link['date_created'] = datetime.fromtimestamp(raw_add_date).replace(tzinfo=timezone.utc)
                        elif attr == 'PRIVATE':
                            link['private'] = 0 if value_found == '0' else 1
                        elif attr == 'TAGS':
                            link['tags'] = value_found

                    if link['url'] != '' and link['url']:

                        if reload_article_from_url:
                            if link['url'].startswith('?'):
                                continue
                            link['title'], link['text'], link['image'], link['video'] = grab_full_article(link['url'])

                        if private:
                            link['private'] = 1

                        table.add_row(link['title'],
                                      "Yes" if link['private'] else "No",
                                      str(link['date_created']))

                        try:
                            obj = Links.objects.get(url=link['url'])
                            obj.title = link['title']
                            obj.text = link['text']
                            obj.tags = link['tags']
                            obj.private = private
                            obj.date_created = link['date_created']
                            obj.image = link['image']
                            obj.video = link['video']
                            obj.url_hashed = small_hash(link['date_created'].strftime("%Y%m%d_%H%M%S"))
                            msg = f"ShaarPy :: updating {obj.url}"
                            logger.debug(msg)
                            obj.save()
                        except Links.DoesNotExist:
                            new_values = {'url': link['url'],
                                          'url_hashed': small_hash(link['date_created'].strftime("%Y%m%d_%H%M%S")),
                                          'title': link['title'],
                                          'text': link['text'],
                                          'tags': link['tags'],
                                          'private': private,
                                          'date_created': link['date_created'],
                                          'image': link['image'],
                                          'video': link['video'],
                                          }
                            obj = Links(**new_values)
                            obj.save()
                            msg = f"ShaarPy :: creating {obj.url}"
                            logger.debug(msg)

        console.print(table)

# IMPORTING PELICAN FILE


def import_pelican(the_file: str) -> NoReturn:  # noqa: C901
    """
    Headers are :

    Title: Home Sweet Home
    Date: 2021-09-27
    Author: foxmask
    Category: Korea
    Tags: hosting, Korea
    Slug: home-sweet-home
    Status: published
    Summary: text

    body content

    the_file: path of the file to create
    """
    private = 0
    title = ''
    date_created = ''
    slug = ''
    tags = ''
    url_hashed = ''
    text = ''
    status = ''
    summary = ''
    author = ''

    with open(the_file, 'r') as f:
        data = f.readlines()
        msg = f"ShaarPy :: importing {the_file}"
        logger.debug(msg)

        for line in data:
            if line.startswith('Author:'):
                author = line.split('Author: ')[1].strip()
                author = f"</br>By {author}"
            if line.startswith("Status: "):
                status = line.split('Status: ')[1].strip()
            if line.startswith("Title: "):
                title = line.split('Title: ')[1].strip()
            if line.startswith("Date: "):
                date_created = line.split('Date: ')[1].strip()
                if len(date_created) == 10:
                    # date without hours minutes secondes
                    date_created += ' 00:00:00'
                elif len(date_created) == 16:
                    # date with hours minutes
                    date_created += ':00'
                date_created = datetime.strptime(date_created, "%Y-%m-%d %H:%M:%S")

            if line.startswith("Tags: "):
                tags = line.split('Tags: ')[1].strip()

                unwanted_chars = '?./:;!#&@{}[]|`\\^~*+=-_'

                if any(s in unwanted_chars for s in tags):
                    tags = ''

                if tags.endswith(','):
                    tags = tags[:-1]
                tags = tags.replace(' ', '')

            if line.startswith("Slug: "):
                slug = line.split('Slug: ')[1].strip()
            if line.startswith("Summary: "):
                summary = '# ' + line.split('Summary: ')[1] + "\n\n"
            if status == 'published':
                url_hashed = small_hash(date_created.strftime("%Y%m%d_%H%M%S"))
            if not line.startswith(("Status:", "Title:", "Date:", "Tags:", "Slug", 'Status:', 'Summary:')):
                text += summary + line
    if status == 'published':

        try:
            Links.objects.get(url_hashed=url_hashed)
            console.print(f"Shaarpy :: {title} already exists", style="yellow")
        except Links.DoesNotExist:
            Links.objects.create(
                title=title,
                tags=tags,
                url=slug,
                url_hashed=url_hashed,
                text=text,
                date_created=date_created,
                private=private)
            console.print(f"Shaarpy :: {title} added", style="magenta")


def import_pelican_folder(folder: str) -> NoReturn:
    """
    folder: folder path where to find md file to import
    """

    for p in Path(folder).glob('*.md'):
        import_pelican(folder + "/" + p.name)
