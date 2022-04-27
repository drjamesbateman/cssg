# Canvas Static Site Generator

A very simplistic SSG for [Canvas](https://www.instructure.com/) using [canvasapi](https://canvasapi.readthedocs.io/en/stable/getting-started.html) and [pandoc](https://pandoc.org/).

# Pages

Pages are written in [Markdown](https://www.markdownguide.org/getting-started/) and must have the following [TAML](https://en.wikipedia.org/wiki/YAML) header:

```yaml
---
title: Title which matches the filename
---
```

For links between Markdown documents to be interpreted correctly by any sane system and by Canvas, then we must mimic the way in which Canvas converts titles to filenames.  The above would become `title-which-matches-the-filename`.

# Organisation

Create a new folder to store the site.  The folder structure should be:

```
./config.json
./content/...
./content/Modules/...
./content/Discussions/...
./content/Assignments/...
./static/...
```

## config

Obtain an API token as described [here](https://community.canvaslms.com/t5/Admin-Guide/How-do-I-obtain-an-API-access-token-in-the-Canvas-Data-Portal/ta-p/157).

Create the file `config.json` containing the following:

```json
{
  "API_URL" : Full https URL of Canvas,
  "TOKEN"   : API token obtained above,
  "course"  : integer identifying specific Canvas course
  }
```

## content

Pages herein are not associated with a specific module.

## Modules

## Discussions

## Assignments

## static
