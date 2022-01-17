import hashlib
from PIL import Image
import pathlib


def get_hash(filepath: str) -> str:
    """
    Returns the MD5 checksum of a file

    Parameters:
    -----------
        filepath (str): path to file
    Returns:
    --------
        str: hash result
    """
    file = open(filepath, "rb")
    md5_hash = hashlib.md5()
    content = file.read()
    md5_hash.update(content)
    return md5_hash.hexdigest()


def get_shape(filepath: str) -> str:
    """
    Get shape and number dims of image

    Parameters
    ----------
        filepath : str, filename of image
    Returns
    -------
        witdh: int
        height: int
        ndim: int
        readable: bool
    """
    try:
        im = Image.open(filepath)
    except Exception:
        return 0, 0, 0, False
    height, witdh = im.size
    mode = str(im.mode)
    ndim = 1 if len(mode) < 3 else len(mode)
    return witdh, height, ndim, True


def get_size(filepath: str) -> float:
    """
    Get size in kilobytes of image

    Parameters
    ----------
        filepath : str, filename of image
    Returns
    -------
        size : float, size in kb of image
    """
    size = round(pathlib.Path(filepath).stat().st_size * 0.001, 2)
    return size


def get_info(filepath: str, url=None) -> dict:
    """
    Get information about image

    Parameters
    ----------
        filepath : str, filename
    Returns
    -------
        info: dict, dict with informations of file
    """
    w, h, d, r = get_shape(filepath=filepath)
    hash = get_hash(filepath=filepath)
    size = get_size(filepath=filepath)
    return {'hash': hash,
            'filepath': filepath,
            'readable': r,
            'uri': url,
            'witdh': w,
            'height': h,
            'ndim': d,
            'kb': size}
