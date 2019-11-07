# -*- coding: utf-8 -*-

"""
Utility functions.
"""


def get_iter_pages(pages: int, page: int, edge: int=2, around: int=2) -> list:
    """
    Gets the iteration pages to display on the page bottom.
    :param pages: int
    :param page: int
    :param edge: int
    :param around: int
    :return: list
    """
    iter_pages = []
    for i in range(1, pages + 1):
        if i == page or i <= edge or i > pages - edge or i >= page - around or \
                i <= page + around:
            iter_pages.append(i)
    return iter_pages
