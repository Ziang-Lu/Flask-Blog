# -*- coding: utf-8 -*-

"""
Flask main-related routes module.
"""

from flask import Blueprint, render_template, request

from ..models import Post

# Create a main-related blueprint
main_bp = Blueprint(name='main_bp', import_name=__name__)

# Register all the routes on the blueprint


@main_bp.route('/')
@main_bp.route('/home')
def home():
    """
    Home page.
    When a "GET" request is forwarded to "/", this function gets called.
    :return:
    """
    # Pagination (3 posts per page)
    page = request.args.get('page', type=int, default=1)
    posts = Post.query.order_by(Post.date_posted.desc())\
        .paginate(per_page=3, page=page)

    context = {
        'posts': posts
    }
    return render_template('home.html', **context)


@main_bp.route('/about')
def about():
    """
    About page.
    When a "GET" request is forwarded to "/about", this function gets called.
    :return:
    """
    context = {
        'title': 'About'
    }
    return render_template('about.html', **context)

