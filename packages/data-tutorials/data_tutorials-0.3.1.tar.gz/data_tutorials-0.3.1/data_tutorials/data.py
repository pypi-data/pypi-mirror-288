# Author; alin m elena, alin@elena.re
# Contribs;
# Date: 26-07-2024
# ©alin m elena, GPL v3 https://www.gnu.org/licenses/gpl-3.0.en.html
"""
Simple module to download a file from a URL and save it in a specific folder.
"""

from urllib.request import urlretrieve
from pathlib import Path

# this is only for python 3.9 once done use str| list[str]
from typing import Union

DEFAULT_URL = "https://raw.githubusercontent.com/ddmms/data-tutorials/main/data/"


def download_file(url: str, filename: str, dest: Path) -> None:
    save_file = dest / filename
    print(f"try to download {filename} from {url} and save it in {save_file}")
    path, _ = urlretrieve(url + filename, save_file)
    if path.exists():
        print(f"saved in {save_file}")
    else:
        print(f"{save_file} could not be downloaded, check url.")


def get_data(
    url: str = DEFAULT_URL, filename: Union[str, list[str]] = "", folder: str = "data"
) -> None:
    p = Path(folder)
    p.mkdir(parents=True, exist_ok=True)
    if isinstance(filename, str):
        download_file(url, filename, p)
    elif isinstance(filename, list):
        for f in filename:
            download_file(url, f, p)
