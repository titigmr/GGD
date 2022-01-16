from ggd import GoogleImage
from glob import glob
import os
import pathlib
from PIL import Image
from selenium.webdriver.remote.command import Command


def clear_dir(folder):
    for pt in glob(os.path.join(folder, '*')):
        os.remove(pt)
    os.rmdir(folder)


def folder_image_sizes(files):
    shapes = [Image.open(im).size for im in files]
    max_shape = max(max(shapes))
    return max_shape


def read_asset(file):
    with open(file) as f:
        lines = "".join([line.rstrip() for line in f])
    return lines


def get_status(driver):
    status = driver.execute(Command.STATUS)
    return not status["value"]["ready"]


def test_webdriver():
    gg = GoogleImage()
    status_ok = get_status(gg.driver)
    gg.close()
    status_ko = get_status(gg.driver)
    assert status_ok == True
    assert status_ko == False


def test_request():
    gg = GoogleImage()
    gg.get_url(gg.driver, 'Alakazam')
    current_url = gg.driver.current_url
    url = 'https://www.google.fr/search?q=Alakazam&tbm=isch&pws=0'
    gg.close()
    assert current_url == url


def test_download_url():
    gg = GoogleImage()
    dirf = 'Alakazam'
    gg.__setattr__('name', dirf)
    img_url = "https://www.pokepedia.fr/images/6/68/Alakazam-RFVF.png"
    file = gg._download_img(image_url=img_url,
                            name="Alakazam",
                            make_dir=True)
    assert file == 'Alakazam/Alakazam.png'
    assert pathlib.Path('Alakazam/Alakazam.png').is_file()
    clear_dir(dirf)


def test_download_data_uri():
    gg = GoogleImage()
    dirf = 'Alakazam'
    gg.__setattr__('name', dirf)
    img_uri = read_asset(os.path.join('tests', 'assets', 'datauri.txt'))
    file = gg._download_img(image_url=img_uri,
                            name="Alakazam",
                            make_dir=True)
    assert file == 'Alakazam/Alakazam.jpeg'
    assert pathlib.Path('Alakazam/Alakazam.jpeg').is_file()
    clear_dir(dirf)


def test_download_dir_closeaf_witext():
    gg = GoogleImage(close_after_download=False,
                     add_extensions=False)
    dirf = 'Images'
    os.mkdir(dirf)
    one = 'Alakazam'
    two = 'Tortank'
    gg.download(request=one, n_images=1,
                make_dir=False, directory="Images")
    gg.download(request=two, n_images=1,
                make_dir=False, directory="Images")
    gg.close()
    files = glob(os.path.join(dirf, '*'))
    assert 'Images/Alakazam_0' in files
    assert 'Images/Tortank_0' in files
    clear_dir(dirf)


def test_download():
    gg = GoogleImage()
    dirf = 'Alakazam'
    n_images = 10
    gg.download(dirf, n_images=n_images)
    files = glob(os.path.join(dirf, '*'))
    sum_size = sum([pathlib.Path(f).stat().st_size * 0.001 for f in files])
    max_size = folder_image_sizes(files)
    # check if all images are download
    assert n_images == len(files)
    # check if not thumbnails
    assert max_size >= 500
    # check if not empty files
    assert sum_size > 1
    clear_dir(dirf)

