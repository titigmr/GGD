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


def create_webdriver(headless=False, web_driver='firefox', **kwargs):
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


class GoogleImage:
    """
    Google images downloader.

    When parameters is set up, there are available function and attributes:
        - `download()`
        - `close()`
        - `all_files`

    """

    def __init__(self,
                 driver,
                 time_sleep=1,
                 verbose=True,
                 ext_default='.png',
                 close_after_download=True,
                 make_dir=True):
        """
        Download images from Google Image with a webdriver selenium.

            driver: selenium webdriver (Chrome, Firefox or Safari) used to web-scraping.
            time_sleep: time waiting in secondes for scrolling (default: 1)
                    NOTE: If number of images downloaded is not correct, increase this parameter.
            verbose: bool, show progress bar (default: True).
            ext_default: str, when images has no extension, the default extension
                    will be added (default: '.png').
            close_after_download: bool, when download is done, close the webdriver
                            (default: True).
            make_dir: bool, (default: True) create a directory to save images.

        ---
        Use example:
        >>> from selenium import webdriver
        >>> driver = webdriver.Firefox()
        >>> google_dl = GoogleImage(driver=driver)
        >>> request = 'Cat'
        >>> google_dl.download(request=request, n_images=10)

        """
        self.driver = driver
        self.time_sleep = time_sleep
        self.verbose = verbose
        self.all_files = []
        self.ext_default = ext_default
        self.close_after_download = close_after_download
        self.make_dir = make_dir

    def close(self):
        "Close the webdriver."
        self.driver.close()

    def download(self, request, n_images, directory=None, name=None):
        """
        Download images with the webdriver.

        Parameters:
        ----------
        request: str, request searched in google image.
        n_images: int, number of images to download.
        directory: str, where images are downloaded.
        name: str, name of the directory and filenames (default: None).
              If None, the name is given by the value of the request.

        """

        # set des variables
        url = f"https://www.google.fr/search?q={request}&tbm=isch&pws=0"
        n_downloads = 0
        n_unload = 0
        self.valid_extensions = (".png", ".jpg", ".jpeg")
        n_str = len(str(n_images))
        self.name = str(request) if name is None else str(name)

        # get url
        self.get_url(driver=self.driver,
                     request=request)

        # scroll
        self._scroll(driver=self.driver,
                     time_sleep=self.time_sleep,
                     n_images=n_images + 1)

        # get all images
        all_img = self.driver.find_elements(
            by='class name', value='isv-r')[:n_images]

        if self.verbose:
            all_img = tqdm(all_img, desc=self.name, leave=True)

        # download each images
        for im in all_img:
            if self._verify_image(im):
                im.click()
            else:
                if self.verbose:
                    n_unload += 1
                    all_img.set_postfix({'unloaded': n_unload})
                continue

            img_url = self.driver.find_element(by="class name", value='n3VNCb')
            url = img_url.get_attribute('src')
            name_img = f'{self.name}_{n_downloads:0{n_str}d}'
            file = self._download_img(url,
                                      directory=directory,
                                      name=name_img,
                                      ext_default=self.ext_default,
                                      make_dir=self.make_dir)

        # verify download
            if file is not None:
                n_downloads += 1
                self.all_files.append(file)

            if self.verbose and file is None:
                n_unload += 1
                all_img.set_postfix({'unloaded': n_unload})

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
                actualise = driver.find_element(by="class name", value='mye4qd')
                if actualise.size['height'] > 0 and actualise.size['width'] > 0:
                    actualise.click()
                else:
                    break
            last_height = new_height
            if n_images > 0:
                if len(driver.find_elements(
                        by="class name", value='isv-r')) > n_images + 1:
                    break

    def _build_path_name(self, ext, directory, make_dir, name):
        if ext not in self.valid_extensions:
            ext = self.ext_default
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

        NOTE: Need refacto
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
            ext = re.findall('data:image/(.*);', image_url)
            file = self._build_path_name(ext=ext,
                                         name=name,
                                         directory=directory,
                                         make_dir=make_dir)
            try:
                with open(file, "wb") as f:
                    f.write(base64.b64decode(image_url.split('base64')[1]))
            except Exception:
                return None
        else:
            return None
        return file

    def _verify_image(self, element):
        """
        Check if the box is an image
        """
        source_element = element.get_attribute('innerHTML')
        if 'Recherche' in source_element:
            return False
        return True

    def _create_directory(self, path):
        """
        Create a directory where images are saved
        """
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    def _create_path_name(self, directory=None, make_dir=True):
        """
        Build the path name where image is saved
        """
        directory = '' if directory is None else directory
        if make_dir:
            path = os.path.join(directory, self.name)
            return path
        return None
