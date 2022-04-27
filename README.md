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
./content/Modules/...
./content/Assignments/...
./content/Discussions/...
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

## Modules

Pages can either be here or inside a folder here.  If they are inside a folder, then that folder name will be used as a Canvas Module.

For example, in the following `general-information.md` is not associated with a Module and `powder-x-ray-camera.md` is placed inside a Module.

```
general-information.md
Crystallography/powder-x-ray-camera.md
```

Structure of pages within a Canvas module is not controlled, but ordering and indentation should not change when you update page contents.

## Assignments

An existing assignment with the correct name should exist before you try to push contents.  If not, an error will be raised.

## Discussions

This is not yet implemented here; it works elsewhere in more scrappy code.

## static

Thie folder contains HTML created in preparation for upload to Canvas.  It should never store Markdown files and it can be safely deleted.
