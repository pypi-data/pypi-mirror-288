# Soundcloud Scraper
This tool is meant to get metadata from tracks.
Currently, it is only possible to get data from a specific Track.

## What Data?
The Default gets you the cover-art as jpg and the description as txt file.
With the --json flag you can also get following as json.

Instead of downloading files, links will be saved!
```
title: Required[str]
cover_art: Required[str]
genre: Required[str]
buy_link: str
description: Required[list[str]]
```
