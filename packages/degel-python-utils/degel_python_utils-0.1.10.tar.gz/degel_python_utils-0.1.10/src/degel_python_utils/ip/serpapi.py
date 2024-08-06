"""
This module provides functions to interact with the SerpApi.

Functions:
    google_search: Perform a Google search.
    lookup_patent: Lookup a patent using Google Patents.
"""

from typing import Any

from serpapi import GoogleSearch

from degel_python_utils.sys_utils.log_tools import setup_logger

logger = setup_logger(__name__)
# pylint: disable=logging-fstring-interpolation


def google_search(q: str, api_key: str) -> dict[str, Any]:
    """Perform a Google search and return the result as a dictionary.

    Args:
        q: The query string to search for.
        api_key: The API key for authenticating with SerpApi.

    Returns:
        A dictionary containing the search results.
    """
    search = GoogleSearch({"q": q, "api_key": api_key})
    return search.get_dict()


def lookup_patent(q: str, api_key: str) -> dict[str, Any]:
    """Lookup a patent using Google Patents and return the result as a dictionary.

    Args:
        q: The query string to search for patents.
        api_key: The API key for authenticating with SerpApi.

    Returns:
        A dictionary containing the patent search results.
    """
    search = GoogleSearch({"q": q, "engine": "google_patents", "api_key": api_key})
    return search.get_dict()
