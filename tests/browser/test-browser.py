from ggd import GoogleImage
from glob import glob
import os
from selenium.webdriver.remote.command import Command

def clear_dir(folder):
    for pt in glob(os.path.join(folder, '*')):
        os.remove(pt)
    os.rmdir(folder)

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

def test_download():
    gg = GoogleImage()
    dirf = 'Alakazam'
    n_images = 10
    gg.download(dirf, n_images=n_images)
    files = glob(os.path.join(dirf, '*'))
    assert n_images == len(files)
    clear_dir(dirf)