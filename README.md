# Flask Blog

This repo contains the `Flask Blog` project, taught by *Corey Schafer* on his YouTube channel.

Check out: https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=1

<br>

## Tech Stack

**Flask** as backend + **SQLite** as database

* This project uses `WTForms` and `flask_wtf` to implement forms.
* Since this project uses relational database,  `flask-sqlalchemy` module is used for ORM-related tasks, including defining `User` model, which handled registration issues.
* This project uses `flask_login` module to handle user log-in/log-out and authentication issues.

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

***

### About Class-Based View and RESTful API

I could have implemented the routes as class-based views (called "pluggable views" in Flask), or even designed RESTful API for this `Flaskr` project.

=> Follow the steps in the official documentation: https://flask.palletsprojects.com/en/1.1.x/views/ and https://flask.palletsprojects.com/en/1.1.x/api/#class-based-views

<br>

However, considering some facts:

- Flask is a lightweight framework.
- Class-based views in Flask, i.e., "pluggable views", are inspired from Django, and thus are not very popular.

I decide NOT to use class-based views for this project.

***

<br>

## Packaging the Application into a Docker Image

***

Without using Docker, someone may do `git clone` from my GitHub repo, and go through all the environment setup and database initialization steps above, to get this `Flask-Blog` application up and running.

***

To **"build once, run anywhere" using Docker**, we can build this application into a Docker image:

***

*Note that when running the application in its own container, we use Gunicorn, rather than the default Flask developement server.*

***

```bash
$ docker build -t ziangl/flask-blog-app-dev .
```

*Note that since we'll be running the application in its own container, we don't need a whole virtual environment anymore. Thus, we could simply generate a `requirements.txt`:*

```bash
$ pipenv lock -r > requirements.txt
```

*And in the container, install all the dependencies from that.*

On another machine, we can get the Docker image, run a container from the image, and run the `Flask-Blog` application:

```bash
$ docker run -it -p 5000:5000 ziangl/flask-blog-app-dev
```

<br>

## License

This repo is distributed under the <a href="https://github.com/Ziang-Lu/Flask-Blog/blob/master/LICENSE">MIT license</a>.