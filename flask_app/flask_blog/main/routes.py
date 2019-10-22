# -*- coding: utf-8 -*-

"""
Flask main-related routes module.
"""

from flask import Blueprint, render_template, request

from .. import limiter
from ..models import Post

# Create a main-related blueprint
main_bp = Blueprint(name='main', import_name=__name__)
# Rate-limit all the routes registered on this blueprint.
limiter.limit()(main_bp)


@main_bp.route('/')
@main_bp.route('/home')
def home():
    """
    Home page.
    :return:
    """
    # Pagination
    page = request.args.get('page', type=int, default=1)
    p = Post.query.order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=3)
    # "p" is a Pagination object.

    context = {
        'p': p
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
