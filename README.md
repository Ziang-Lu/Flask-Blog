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
> pipenv --python=3.7
> pipenv shell

# Install all the packages specified in Pipfile
> pipenv install
```

<br>

## Database Initialization

Since we use `flask-sqlalchemy` for ORM-related tasks, we need to manually initialize our database and the tables.

Open the terminal and enter Python interactive shell, then do

```python
from flask_blog import db

db.drop_all()
db.create_all()
```

