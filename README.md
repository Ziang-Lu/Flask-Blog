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

## Deploying to Linode

### Linode Linux Server Setup

Create a Linode Linux server, and when logging into that server for the first time

* Update the installed softwares

  ```bash
  $ apt update && apt upgrade
  ```

* Set up the hostname

  ```bash
  $ hostnamectl set-hostname flask-blog-server
  # Check it out
  $ hostname
  flask-blog-server
  ```

  Also modify the `hosts` file

  ```bash
  $ vi /etc/hosts
  
  # Right under "127.0.0.1", add the following line
  <Linode IP address>	flask-blog-server
  ```

* Create a new user (rather than doing everything as `root`)

  ```bash
  $ adduser ziang
  ```

  Add the new user to the `sudo` group, so that it can run admin commands

  ```bash
  $ adduser ziang sudo
  ```

  Log out of the server, and log back in as the new user

  ```bash
  $ exit
  
  # On local machine
  $ ssh ziang@<Linode IP address>
  ```

Then, do the following

* Use SSH key-based authentication (rather than typing passwords all the time)

  ```bash
  # On local machine
  
  $ ssh-keygen -b 4096
  # Copy the public key to the server
  $ scp ~/.ssh/id_rsa.pub ziang@<Linode IP address>:~/.ssh/authorized_keys
  ```

* Change some permission-related stuff on the server

  ```bash
  $ sudo chmod 700 ~/.ssh/
  $ sudo chmod 600 ~/.ssh/*
  ```

* Finally, we no longer need to user `root` user.

  Disallow `root` log-in through SSH key-based authentication

  ```bash
  $ sudo vi /etc/ssh/sshd_config
  
  # Set the following
  PermitRootLogin no
  PasswordAuthentication no
  ```

  Restart SSHD service to activate the changes

  ```bash
  $ sudo systemctl restart sshd
  ```

### Flask Application Deployment

On the server

* Clone the GitHub repo

  ```bash
  $ git clone https://github.com/Ziang-Lu/Flask-Blog.git
  ```

* Install Python 3, `pip`, `venv` and `Pipenv`

  ```bash
  $ apt install python3-pip
  $ apt install python3-venv
  $ apt install pipenv
  ```

* Follow the steps in "Environment Setup" to set up the environment

**Deploy the Flask application to a production server**

* Install Nginx and Gunicorn

  ```bash
  $ apt install nginx
  $ apt install gunicorn3  # For letting Gunicorn use Python 3
  ```

* Nginx + Gunicorn

  ```bash
  # Delete the default Nginx configuration file
  $ sudo rm /etc/nginx/sites-enabled/default
  
  $ sudo vi /etc/nginx/sites-enabled/flask-blog
  ```

  ***

  *How do Nginx and Gunicorn work together?*

  * *Nginx handles static information (like CSS files, JavaScript-related codes, pictures, etc.)*
  * *Gunicorn runs on the server and listens on port 8000.*
  * *Nginx forwards Flask requests to Gunicorn, and let Gunicorn handle Python/Flask-related codes*

  ***

  Write the following:

  ```nginx
  server {
      listen 80;
      server_name <Linode IP address>;
  
      # Nginx handles static information (like CSS files, JavaScript-related codes, pictures, etc.)
      location /static {
          alias /home/ziang/Flask-Blog/flask_blog/static;
      }
  
      # Forward Flask requests to Gunicorn, and let Gunicorn handle Python/Flask-related codes
      location / {
          # Gunicorn runs on the server and listens on port 8000.
          proxy_pass http://localhost:8000;
          include /etc/nginx/proxy_params;
          proxy_redirect off;
      }
  }
  ```

* Start Nginx

  ```bash
  $ sudo systemctl restart nginx
  ```

  ***

  After Nginx started, if we go to `http://<Linode-IP-address>`, we can see an Nginx error page, because it forwards that request to Gunicorn, but we haven't started Gunicorn.

  However, if we go to `http://<Linode-IP-address>/static/main.css`, we are able to see that file, because Nginx handles static information, as we set up above.

  ***

  Start Gunicorn

  ```bash
  $ cd Flask-Blog
  
  # Note that since we only have 1 CPU, we choose #ofWorkers = #ofCores * 2 + 1 = 3
  $ gunicorn3 -w 3 "flask_blog:create_app()"
  ```

