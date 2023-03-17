import requests
import zipfile
from pathlib import Path
from os.path import expandvars


def as_expanded_path(path: str) -> Path:
    return Path(expandvars(path)).resolve()


def download_from_url(url: str, destination: str) -> str:
    fetched_file = requests.get(url)
    with open(as_expanded_path(destination), "wb") as f:
        f.write(fetched_file.content)


def unzip(file_to_unzip: str, destination: str):
    with zipfile.ZipFile(as_expanded_path(file_to_unzip), 'r') as zip_f:
        zip_f.extractall(as_expanded_path(destination))
