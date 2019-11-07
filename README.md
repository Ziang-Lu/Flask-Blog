# Flask Blog

This repo contains the `Flask Blog` project, taught by *Corey Schafer* on his YouTube channel.

Check out: https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=1

<br>

## Tech Stack

**Flask** as backend framework + **PostgreSQL** as database

* This project uses `WTForms` and `Flask-WTF` to implement forms.
* Since this project uses relational database,  `Flask-SQLAlchemy` module is used for ORM-related tasks, including defining `User` model, which handled registration issues.
* This project uses `Flask-Login` module to handle user log-in/log-out and authentication issues.

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

## Running the Flask Application

```bash
$ ./run.sh
```

Then simply go to http://localhost:5000

<br>

## License

This repo is distributed under the <a href="https://github.com/Ziang-Lu/Flask-Blog/blob/master/LICENSE">MIT license</a>.