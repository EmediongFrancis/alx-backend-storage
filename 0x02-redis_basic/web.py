#!/usr/bin/env python3
""" Module for Implementing an expiring web cache and tracker """

from functools import wraps
import redis
import requests
from typing import Callable

r = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """ Decortator for counting how many times a request
    has been made """

    @wraps(method)
    def wrapper(url):
        """ Wrapper for decorator functionality """
        r.incr(f"count:{url}")
        if cached_html := r.get(f"cached:{url}"):
            return cached_html.decode('utf-8')

        html = method(url)
        r.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """Uses the requests module to obtain the HTML
    content of a particular URL and returns it.
    """
    req = requests.get(url)
    return req.text
