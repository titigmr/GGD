import hashlib

def get_hash(filepath: str) -> str:
    """Returns the MD5 checksum of a file
    Args:
        filepath (str): path to file
    Returns:
        str: hash result
    """
    my_file = open(filepath, "rb")
    md5_hash = hashlib.md5()
    content = my_file.read()
    md5_hash.update(content)
    return md5_hash.hexdigest()

