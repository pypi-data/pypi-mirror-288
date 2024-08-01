from argparse import ArgumentParser, Namespace

from bs4 import BeautifulSoup
import requests

from typing import Literal, Required, TypedDict
import json
from os.path import exists

import sys

arg_parser = ArgumentParser()
arg_parser.add_argument("url", type=str, help="URL from a track.")
arg_parser.add_argument("--html", action='store_true', help="download index.html")
arg_parser.add_argument("--json", action='store_true', help="Safe output as JSON")
arg_parser.add_argument("--User-Agent", type=str, help="set custom User-Agent string.")
arg_parser.add_argument("-v", "--verbose", action='store_true', help="enable verbose mode.")

args: Namespace = arg_parser.parse_args()


class SoundcloudTrack(TypedDict, total=False):
    title: Required[str]
    cover_art: Required[str]
    genre: Required[str]
    buy_link: str
    description: Required[list[str]]


def download_html():
    if exists("../index.html"):
        return
    soup = BeautifulSoup(session.get(args.url).content, 'html.parser')

    with open('../index.html', 'w') as file:
        file.write(soup.prettify())
        file.close()


def download_cover_art(title: str, url: str):
    response = session.get(url)

    if response.status_code != 200:
        sys.stderr.write(f"Couldn't download cover art for {url}\n")
        return
    with open(f'{title}.jpg', 'wb') as file:
        file.write(response.content)


def download_description(title: str, description: list[str]):
    with open(f'{title}.txt', 'w') as file:
        for line in description:
            file.write(line + "\n")


def extract_title(soup: BeautifulSoup) -> str:
    title = soup.find(attrs={"property": "og:title"})
    if title is None:
        sys.stderr.write("Title not found!\n")
        sys.exit(1)
    return title.get('content').strip()


def extract_cover_art(soup: BeautifulSoup) -> str:
    cover_art = soup.find(attrs={"property": "og:image"})
    if cover_art is None:
        sys.stderr.write("Cover art not found!\n")
        sys.exit(1)
    return cover_art.get('content').strip()


def extract_genre(soup: BeautifulSoup) -> str:
    genre = soup.find(attrs={"itemprop": "genre"})
    if genre is None:
        sys.stderr.write("Genre not found!\n")
        sys.exit(1)
    return genre.get('content').strip()


def extract_description(soup: BeautifulSoup) -> list[str]:
    description = soup.find(attrs={"itemprop": "description"})
    if description is None:
        sys.stderr.write("Description not found!\n")
        sys.exit(1)
    return description.get('content').strip().split('\n')


def extract_buy_link(footer: BeautifulSoup) -> str | None:
    for tag in footer.find_all('a'):
        return tag.get('href')
    return None


def import_html() -> BeautifulSoup | None:
    with open('../index.html', 'r') as file:
        if file.readable():
            return BeautifulSoup(file, 'html.parser')
    sys.stderr.write("HTML file not found!\n")
    return None


session = requests.Session()
if args.User_Agent:
    session.headers.update({'User-Agent': args.user_agent})


if __name__ == '__main__':
    if args.html:
        download_html()
        beautiful_soup = import_html()
    else:
        beautiful_soup = BeautifulSoup(session.get(args.url).content, 'html.parser')

    if beautiful_soup is None:
        sys.stderr.write("Failed to load html!\n")
        sys.exit(1)

    sc_track: SoundcloudTrack = {
        "title": extract_title(beautiful_soup),
        "cover_art": extract_cover_art(beautiful_soup),
        "genre": extract_genre(beautiful_soup),
        "description": extract_description(beautiful_soup)
    }

    beautiful_soup_footer = beautiful_soup.find('footer')
    buy_link = extract_buy_link(beautiful_soup_footer)
    if buy_link:
        sc_track['buy_link'] = buy_link

    if args.json:
        # Specify the filename for the JSON file
        filename = f'{sc_track.get("title")}.json'

        # Write the sc_track dictionary to a JSON file
        with open(filename, 'w') as json_file:
            json.dump(sc_track, json_file, indent=4)
            json_file.close()

        print(f"SoundCloud track data has been written to {filename}")
        exit(0)

    download_cover_art(sc_track["title"], sc_track["cover_art"])
    download_description(sc_track["title"], sc_track["description"])
    if args.verbose:
        print(json.dumps(sc_track, indent=4))
