"""
Extracted from main to avoid importing pywikibot for the tests
"""

import re
from typing import List

from pywikibot.exceptions import APIError
from yarl import URL


def parse_filter_list(text: str) -> List[str]:
    r = re.compile(r"(Q\d+)\s*(#.*)?")
    filterlist = []
    for line in text.split():
        fullmatch = r.fullmatch(line)
        if fullmatch:
            filterlist.append(fullmatch.group(1))
    return filterlist


def github_repo_to_api(url: str) -> str:
    """Converts a GitHub repository url to the api entry with the general information"""
    url = normalize_url(url)
    url = url.with_host("api.github.com").with_path("/repos" + url.path)
    return str(url)


def github_repo_to_api_releases(url: str) -> str:
    """Converts a GitHub repository url to the api entry with the releases"""
    url = github_repo_to_api(url)
    url += "/releases"
    return url


def github_repo_to_api_tags(url: str) -> str:
    """Converts a GitHub repository url to the api entry with the tags"""
    url = github_repo_to_api(url)
    url += "/git/refs/tags"
    return url


def normalize_url(url: str) -> URL:
    """Canonical urls be like: https, no slash, no file extension"""
    url = URL(url).with_scheme("https").with_fragment(None)
    if url.path.endswith(".git"):
        url = url.with_path(url.path[:-4])
    return url


def is_edit_conflict(error: APIError) -> bool:
    """This is a frequent error for some reason"""
    if messages := error.other.get("messages"):
        for message in messages:
            if message.get("name") == "edit-conflict":
                return True
    return False
