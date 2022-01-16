from setuptools import setup, find_packages


REQUIRED_PACKAGES = [
    'tqdm==4.62.3',
    'requests==2.27.1',
    'selenium==4.1.0',
]

setup(
    name="ggd",
    version='0.3.0',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    description='Google Image Downloader'
)
