# My Flet App

A cross-platform application built with [Flet](https://flet.dev), targeting Android and Web.

## Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation)

## Setup

Install dependencies:

```bash
poetry install
```

## Running

**Headless web server (default — works in containers, port 8550):**
```bash
PYTHONPATH=src poetry run python src/my_flet_app/main.py
```

**Open in browser automatically:**
```bash
FLET_VIEW=web PYTHONPATH=src poetry run python src/my_flet_app/main.py
```

## Building for Android

Requires Flutter SDK and Android SDK installed on your machine.

Install Flutter: https://docs.flutter.dev/get-started/install

Then build the APK:

```bash
poetry run flet build apk
```

Or build an Android App Bundle for the Play Store:

```bash
poetry run flet build aab
```

The output will be in `build/apk/` or `build/aab/` respectively.

## Building for Web

```bash
poetry run flet build web
```

Output is written to `build/web/`. Serve it with any static file host.
