# -*- coding: utf-8 -*-

"""
Flask main-related routes module.
"""

from datetime import datetime

import requests
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from ..utils import get_iter_pages

# Create a main-related blueprint
main_bp = Blueprint(name='main', import_name=__name__)


@main_bp.route('/')
@main_bp.route('/home')
def home():
    """
    Home page.
    :return:
    """
    # TODO: Analyze this method
    page = request.args.get('page', type=int, default=1)

    request_url = f'http://post_service:8000/posts?page={page}&per_page=5'

    username = request.args.get('user')
    if username:
        # Try to fetch all the posts by all the users that this user follows as
        # well as this user himself
        if not current_user.is_authenticated:
            flash('Please log in first.', category='danger')
            return redirect(url_for('auth.login'))
        elif current_user.username != username:
            flash(
                'You can only view your own followed posts.', category='danger'
            )
            return redirect(url_for('main.home', user=current_user.username))
        request_url += f'&user={username}'

    r = requests.get(request_url)
    paginated_data = r.json()
    posts_data = paginated_data['data']['posts']
    # Convert the datetime strings back to objects
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
