import requests
from pathlib import Path
from os.path import expandvars


def download_from_url(url: str, destination: str):
    fetched_file = requests.get(url)
    with open(Path(expandvars(destination)).resolve(), "wb") as f:
        f.write(fetched_file.content)

