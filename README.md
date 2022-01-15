# Google Image Downloader

![pypi](https://github.com/titigmr/GGD/actions/workflows/pip-publish.yml/badge.svg)

Usefull package for collecting image label in machine learning usecases.

## Setup

This package is available on pypi repository

```
pip install ggd
```

Is required using a webdriver ([Geckodriver](https://github.com/mozilla/geckodriver/releases), [Chromedriver](https://chromedriver.chromium.org/downloads), etc...) and have the executable in the path.

The folowing command can be used in linux64 platform

```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz && tar -zxvf geckodriver-v0.30.0-linux64.tar.gz && rm geckodriver-v0.30.0-linux64.tar.gz && mv geckodriver /usr/local/bin/
```


## Simple Usage


```python
from ggd import GoogleImage

gg = GoogleImage()
gg.download(request='Alakazam', n_images=200)
```
- All images are downloaded in a new folder.

- `all_files` attribute contains all images pathes downloaded.

```python
print(gg.all_files)
>>> ['Alakazam/Alakazam_000.png',
    'Alakazam/Alakazam_001.png',
    'Alakazam/Alakazam_002.png',
    'Alakazam/Alakazam_003.png',
    'Alakazam/Alakazam_004.png',
    ...]
```

## Advanced Usage

For using this package with more requests labeled and see scraping working in backend.

```python
from ggd import GoogleImage

google_dl = GoogleImage(driver=driver,
                        verbose=True,
                        close_after_download=False,
                        headless=False)

n = 500
for rq, name_im in [("bulbasaur --cards", 'Bulbizarre'),
                    ('ivysaur --cards', 'Herbizarre')]:
    google_dl.download(request=rq,
                       n_images=n,
                       directory='Data',
                       name=name_im)
google_dl.close()
```

For multiplying number and variety of images, use [Google filtering](https://www.numipage.com/mieux-chercher-sur-google-avec-les-filtres-et-les-operateurs-de-recherche/)* in requests , synonyms, other languages...

**article in french*
