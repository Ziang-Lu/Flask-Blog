# -*- coding: utf-8 -*-

"""
Flask main-related routes module.
"""

import requests
from flask import Blueprint, render_template, request

from .. import RATELIMIT_DEFAULT, limiter
from ..utils import get_iter_pages

# Create a main-related blueprint
main_bp = Blueprint(name='main', import_name=__name__)
# Rate-limit all the routes registered on this blueprint.
limiter.limit(RATELIMIT_DEFAULT)(main_bp)


@main_bp.route('/')
@main_bp.route('/home')
def home():
    """
    Home page.
    :return:
    """
    page = request.args.get('page', type=int, default=1)
    r = requests.get(
        f'http://user_post_service:8000/posts?page={page}&per_page=3'
    )
    paginated_data = r.json()
    pages = paginated_data['pagination_meta']['pages']

    context = {
        'p': {
            'items': paginated_data['data'],
            'page': page,
            'pages': pages,
            'total': paginated_data['pagination_meta']['total'],
            'iter_pages': get_iter_pages(pages, page)
        }
    }
    return render_template('home.html', **context)


@main_bp.route('/about')
def about():
    """
    About page.
    :return:
    """
    context = {
        'title': 'About'
    }
    return render_template('about.html', **context)
