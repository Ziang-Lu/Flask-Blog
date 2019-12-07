# -*- coding: utf-8 -*-

"""
Flask main-related routes module.
"""

from datetime import datetime

import flask_login
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

    if flask_login.current_user.is_authenticated:
        r = requests.get(
            f'http://post_service:8000/posts?user='
            f'{flask_login.current_user.username}&page={page}&per_page=5'
        )
    else:
        r = requests.get(
            f'http://post_service:8000/posts?page={page}&per_page=5'
        )
    paginated_data = r.json()
    posts_data = paginated_data['data']
    for post in posts_data:
        post['date_posted'] = datetime.fromisoformat(post['date_posted'])
    pages = paginated_data['pagination_meta']['pages']

    context = {
        'p': {
            'items': posts_data,
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
