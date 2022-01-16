"""
Module for webscraping images using Google image navigator
"""

import requests
import os
import re
import pathlib
import base64
import pathlib
import time

import selenium
from tqdm import tqdm
from selenium import webdriver

from .config import Config
from .exceptions import HTMLError


class GoogleImage:
    """
    Google images downloader.

    When parameters is set up, there are available function and attributes:
        - `download()`
        - `close()`
        - `all_files`

    """

    def __init__(self,
                 driver=None,
                 time_sleep=1,
                 verbose=True,
                 add_extensions=True,
                 ext_default='.png',
                 close_after_download=True,
                 **kwargs):
        """
        Download images from Google Image with a webdriver selenium.

            driver: selenium webdriver (Chrome, Firefox or Safari) used to web-scraping
                    if driver is None use the function `create_webdriver` with kwargs
            time_sleep: time waiting in secondes for scrolling (default: 1)
            verbose: bool, show progress bar (default: True).
            add_extensions: bool, if True add extensions finded in url, else
                            save image without extensions (default: True)
            ext_default: str, when images has no extension, the default extension
                        will be added (default: '.png'). Must had `add_extensions` as True.
            close_after_download: bool, when download is done, close the webdriver
                                (default: True).

        ---
        Use example:
        >>> from ggd import GoogleImage
        >>> google_dl = GoogleImage()
        >>> request = 'Cat'
        >>> google_dl.download(request=request, n_images=10)

        """
        if 'config' not in kwargs :
            self.config = Config()
        else:
            self.config = kwargs["config"]
            kwargs.pop('config')

        self.driver = create_webdriver(**kwargs) if driver is None else driver
        self.time_sleep = time_sleep
        self.verbose = verbose
        self.all_files = []
        self.ext_default = ext_default
        self.close_after_download = close_after_download
        self.name = ''
        self.add_extensions = add_extensions

    def close(self):
        "Close the webdriver."
        self.driver.close()

    def download(self, request, n_images, directory=None, name=None,
                 make_dir=True):
        """
        Download images with the webdriver.

        Parameters:
        ----------
        request: str, request searched in google image.
        n_images: int, number of images to download, if value
                  is -1, select all images in the page.
        directory: str, where images are downloaded.
        name: str, name of the directory (if make_dir is True)
              and filenames (default: None).
              If None, the name is given by the value of the request.
        make_dir: bool, (default: True) create a directory to save images.

        """

        # set des variables
        url = f"https://www.google.fr/search?q={request}&tbm=isch&pws=0"
        n_downloads = 0
        n_unload = 0
        n_str = len(str(n_images))
        self.name = str(request) if name is None else str(name)

        # get url
        self.get_url(driver=self.driver,
                     request=request)

        # scroll
        n_finded = self._scroll(driver=self.driver,
                                time_sleep=self.time_sleep,
                                n_images=n_images)

        # show popup
        self.driver.find_element(
            by='class name', value=self.config.BLOC_IMAGE).click()

        # skip first because is a thumbnail
        self.driver.find_element(by='xpath',
                                 value=self.config.BLOC_AFTER).click()

        all_img = range(n_finded)

        if not all_img:
            raise HTMLError(name='BLOC_IMAGE', html=self.config.BLOC_IMAGE)

        if self.verbose:
            all_img = tqdm(all_img, desc=self.name, leave=True)

        # download each images
        for _ in all_img:
            element = self.driver.find_element(
                by="class name", value=self.config.BLOC_POP)
            url = element.get_attribute('src')
            if url is None:
                raise HTMLError(name='BLOC_POP', html=self.config.BLOC_POP)
            name_img = f'{self.name}_{n_downloads:0{n_str}d}'
            file = self._download_img(url,
                                      directory=directory,
                                      name=name_img,
                                      make_dir=make_dir)

            # verify download
            if file is not None:
                n_downloads += 1
                self.all_files.append(file)

            if self.verbose and file is None:
                n_unload += 1
                all_img.set_postfix({'unloaded': n_unload})

            self.driver.find_element(by='xpath',
                                     value=self.config.BLOC_AFTER).click()

        if self.close_after_download:
            self.close()

    def get_url(self, driver, request):
        """
        Get url
        """
        url = f"https://www.google.fr/search?q={request}&tbm=isch&pws=0"
        driver.get(url)

    def _scroll(self, driver, time_sleep=1, n_images=-1):
        """
        Scroll until end of page or image number required
        """
        last_height = driver.execute_script(
            "return document.body.scrollHeight")

        while True:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(time_sleep)
            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                try:
                    actualise = driver.find_element(
                        by="class name", value=self.config.BLOC_END)
                except:
                    raise HTMLError(name='BLOC_END', html=self.config.BLOC_END)
                if actualise.size['height'] > 0 and actualise.size['width'] > 0:
                    actualise.click()
                else:
                    n_finded = len(driver.find_elements(
                        by="class name", value=self.config.BLOC_IMAGE))
                    return n_finded

            last_height = new_height

            if n_images >= 0:
                n_finded = len(driver.find_elements(
                    by="class name", value=self.config.BLOC_IMAGE))
                if not n_finded:
                    raise HTMLError(name='BLOC_IMAGE',
                                    html=self.config.BLOC_IMAGE)
                if n_finded > n_images:
                    return n_images

    def _build_path_name(self, ext, directory, name, make_dir):
        if ext not in self.config.VALID_EXTENSION:
            ext = self.ext_default
        if not self.add_extensions:
            ext = ''
        name += ext
        path = self._create_path_name(directory=directory,
                                      make_dir=make_dir)
        if path is not None:
            self._create_directory(path)
            file = os.path.join(path, name)
        else:
            file = name
        return file

    def _download_img(self,
                      image_url,
                      name,
                      directory=None,
                      make_dir=True):
        """
        Download image with an image url or a base64 encoded binary
        """
        if 'http' in image_url:
            ext = pathlib.Path(image_url).suffix
            file = self._build_path_name(ext=ext,
                                         name=name,
                                         directory=directory,
                                         make_dir=make_dir)
            try:
                with open(file, "wb") as f:
                    f.write(requests.get(image_url).content)
            except Exception:
                return None

        elif 'base64' in image_url:
            ext = '.' + re.findall('data:image/(.*);', image_url)[0]
            file = self._build_path_name(ext=ext,
                                         name=name,
                                         directory=directory,
                                         make_dir=make_dir)
            try:
                with open(file, "wb") as f:
                    f.write(base64.b64decode(image_url.split('base64,')[1]))
            except Exception:
                return None
        else:
            return None
        return file

    def _create_directory(self, path):
        """
        Create a directory where images are saved
        """
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    def _create_path_name(self, directory=None, make_dir=True):
        """
        Build the path name where image is saved
        """
        if make_dir:
            directory = '' if directory is None else directory
            path = os.path.join(directory, self.name)
            return path
        return directory


def create_webdriver(headless=True, web_driver='firefox', **kwargs):
    """
    Create an webdriver object

    Params:
    ----
        headless: bool, scraping without seeing browser (default False)
        webdriver: str, choice of webdriver (default 'firefox')
        **kwargs: other parameters for webdriver
    """
    options = getattr(webdriver, web_driver).options.Options()

    if headless:
        options.add_argument('--headless')

    pager = getattr(
        webdriver, web_driver.capitalize())(
        options=options, **kwargs)
    return pager
