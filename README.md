# Google Image Downloader

Usefull package for collecting image label in machine learning usecases.

## Setup

This package is available on pypi repository

```
pip install ggd
```

## Simple Usage


```python
from ggd import create_webdriver, GoogleImage

driver = create_webdriver()
gg = GoogleImage(driver, time_sleep=2)
gg.download(request='Alakazam', n_images=200)
```
- All images are downloaded in a new folder.

- `time_sleep` parameter is using for scrolling and update the browser. If number of images downloaded is not correct, increase this parameter.

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

## Advanced usage

For using this package with more requests labeled and scraping wotking in backend.

```python
driver = webdriver.Firefox(headless=True)
google_dl = GoogleImage(driver=driver,
                        verbose=True,
                        close_after_download=False)

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

**link in french*