import gzip
import bz2
import re

def decompress_file(file_path):
    if file_path.endswith(".gz"):
        return gzip.open(file_path, "rt")
    elif file_path.endswith(".bz2"):
        return bz2.open(file_path, "rt")
    return open(file_path, "r")

def sanitize_url(url):
    return url.strip().lower()

def is_valid_timestamp(timestamp):
    return re.match(r"^\d{14}$", timestamp) is not None