# Flask Blog

This repo contains the `Flask Blog` project, taught by *Corey Schafer* on his YouTube channel.

Check out: https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=1

<br>

## Tech Stack

*Rate limiting:*

*All routes are protected by rate limiting, implemented with `Flask-Limiter` and `Redis`.*

<br>

## Environment Setup

```bash
$ pipenv --python=3.7
$ pipenv shell

# Install all the packages specified in Pipfile
$ pipenv install
```

<br>

## Database Initialization

We initialize the dabatase directly from the code, as follows (from `flask_blog/__init__.py`)

```python
# ...

def create_app():
    # ...

    with app.app_context():
        db.create_all()

    # ...

# ...
```

<br>

## Tech Stack (Implementation Notes)

<img src="https://github.com/Ziang-Lu/Flask-Blog/blob/master/Flask-Blog%20RESTful%20Architecture.png?raw=true">

We separate `user_post_service` out as a Flask-based web service:

* `user_post_service` is responsible for all the logics and information related to users and their posts, and talks to `PostgreSQL` directly.
  * This web service can be implemented in two ways: check out https://github.com/Ziang-Lu/RESTful-with-Flask/blob/master/Bookstore%20Web%20Service%20Documentation.md. Here we simply use `Flask-RESTful` framework to implement this web service.
  * `Marshmallow/Flask-Marshmallow` is used for schema definition & deserialization (including validation) / serialization.
  * Since this web service is backed by `PostgreSQL` database. And thus `Flask-SQLAlchemy` module is used for ORM-related tasks.

***

* *Why not go one step further, and separate `user_service` or `post_service` out?*

  *Well... we could've done that, but it requires a little bit more effort.*

  *This is because `User` and `Post` has a tightly-coupled 1-to-many relationship, so separating them to different services leads to great inconvenience:*

  *-> A `Post` object has an attribute of `author`, which refers to a `User` object. Imagine we try to separate them out into different services, then in order to pass the representations of `User` and `Post` objects, we have to repeatedly define `UserSchema` and `PostSchema` in both `user_service` and `post_service`, which is redundant and violates the DIY principle.*

***

The communication between the main Flask-Blog app and the web service is through RESTful API, via `JSON`.

<br>

In this way, the original Flask-Blog app now becomes a "skeleton" or a "gateway", which talks to `user_post_service`, uses the fetched data to render HTML templates.

* The main Flask-Blog app uses `WTForms` and `Flask-WTF` to implement forms.

***

*REST架构中要求client-server的communication应该是"无状态"的, 即一个request中必须包含server (service)处理该request的全部信息, 而在server-side不应保存任何与client-side有关的信息, 即server-side不应保存任何与某个client-side关联的session.*

*=> 然而, 我们应该区分"resource state"和"application state": REST要求的无状态应该是对resource的处理无状态, 然而在main application本身里面我们需要保存应用状态, 即user的login和session等.*

***

Thus, in the original Flask-Blog app, we still use `Flask-Login` to handle user log-in/log-out and authentication issues, as well as session management.

<br>

## License

This repo is distributed under the <a href="https://github.com/Ziang-Lu/Flask-Blog/blob/master/LICENSE">MIT license</a>.