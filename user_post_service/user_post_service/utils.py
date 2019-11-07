# -*- coding: utf-8 -*-

"""
Utility functions.
"""

import functools
from typing import Callable

from flask import request
from flask_marshmallow import Schema

from .models import Post


def paginate(collection_schema: Schema, max_per_page: int=10) -> Callable:
    """
    Pagination decorator, with the collections serialized using the given
    collection schema.
    :param collection_schema: Schema
    :param max_per_page: int
    :return: Callable
    """
    def decorated(f: Callable) -> Callable:

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            page = request.args.get('page', type=int, default=1)
            per_page = min(
                request.args.get('per_page', type=int, default=10), max_per_page
            )

            result = f(*args, **kwargs)
            if type(result) == tuple:
                return result
            query = result
            p = query.order_by(Post.date_posted.desc())\
                .paginate(page=page, per_page=per_page)
            # "p" is a Pagination object.

            # Populate the pagination metadata
            pagination_meta = {
                'page': page,
                'pages': p.pages,
                'total': p.total
            }

            return {
                'status': 'success',
                'data': collection_schema.dump(p.items),
                'pagination_meta': pagination_meta
            }, 200
        return wrapper

    return decorated
