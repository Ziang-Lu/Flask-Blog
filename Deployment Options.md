## Deployment Options

### 1. VPS + Web Server + Python Web App WSGI Server

***

For VPS hosting:

* AWS EC2
* Azure
* **Linode**
* Heroku
* DigitalOcean
* InMotion
* Bluehost
* Hostgator

For web server:

* **Nginx**

For Python web app WSGI server:

* **Gunicorn**
* Waitress
* uWSGI

***

How do **Nginx** and **Gunicorn** work together?

* Nginx handles static information (like CSS files, JavaScript-related codes, pictures, etc.)
* Gunicorn runs on the server and listens on port 8000.
* Nginx forwards Flask requests to Gunicorn, and let Gunicorn handle Python/Flask-related codes

***

#### Linode Linux Server Setup

Create a Linode Linux server, and when logging into that server for the first time

* Update the installed softwares

  ```
  $ apt update && apt upgrade
  ```

* Set up the hostname

  ````bash
  $ hostnamectl set-hostname flask-blog-server
  
  # Check it out
  $ hostname
  flask-blog-server
  ````

  Also modify the `hosts` file

  ```bash
  $ sudo vi /etc/hosts
  
  # Right under "127.0.0.1"
  <Linode IP address> flask-blog-server
  ```

* Create a new user (rather than doing everything as `root`)

  ```bash
  $ adduser ziang
  ```

  Add the new user to `sudo` group, so that it can run admin commands

  ```bash
  $ adduser ziang sudo
  ```

  Log out of the server, and log back in as the new user

  ```
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

* Finally, we no longer need to use `root` user.

  Disallow `root` log-in through SSH key-based authentication

  ```bash
  $ sudo vi /etc/ssh/sshd_config
  
  # Set the following
  PermitRootLogin no
  PasswordAuthentication no
  ```

  Restart `sshd` service to activate the changes

  ```bash
  $ sudo systemctl restart sshd
  ```

#### Flask Application Deployment

On the server

* Clone the GitHub repo

* Install Python 3, `pip`, `venv` and `Pipenv`

  ```bash
  $ apt install python3-pip python3-venv
  $ apt install pipenv
  ```

* Follow the steps in "Environment Setup" in `README.md` to set up the environment

**Nginx + Gunicorn**

* Install Nginx and Gunicorn

  ```bash
  $ apt install nginx
  $ pipenv install gunicorn
  ```

* Nginx + Gunicorn

  ```bash
  # Delete the default Nginx configuration file
  $ sudo rm /etc/nginx/sites-enabled/default
  
  # Instead, create a new one
  $ sudo vi /etc/nginx/sites-enabled/flask-blog
  ```

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
  $ gunicorn -w 3 "flask_blog:create_app()"
  ```

* Use `supervisor` to manage the Flask application process

  ***

  *`supervisor` is a client-server system:*

  - *`supervisord` is the server-side running the application, and is responsible for responding commands from the client-side `supervisorctl`*
  - *`supervisorctl` is the client-side for a user, sending control commands to the server-side `supervisord`*

  ***

  ```bash
  $ apt install supervisor
  ```

  Create a `supervisor` configuration file; this configuration file will be used by `supervisord`, running the corresponding programs

  ```bash
  $ sudo vi /etc/supervisor/conf.d/flask-blog.conf
  ```

  Write the following:

  ```
  [program:flask-blog]
  directory=/home/ziang/Flask-Blog/
  command=<full/path/to/gunicorn> -w 3 "flask_blog:create_app()"
  autostart=true
  autorestart=true
  stopasgroup=true
  killasgroup=true
  stdout_logfile=/var/log/flask-blog/flask-blog.out.log
  stderr_logfile=/var/log/flask-blog/flask-blog.err.log
  ```

  Create the corresponding log files:

  ```bash
  $ sudo mkdir -p /var/log/flask-blog
  $ sudo touch /var/log/flask-blog/flask-blog.out.log
  $ sudo touch /var/log/flask-blog/flask-blog.err.log
  ```

  Reload `supervisor` to activate the configurations

  ```bash
  $ sudo supervisorctl reload
  ```

<br>

### 2. Linux Server + Web Server (in `Docker` Container) + Python Web App WSGI Server (in `Docker` Container)

**=> In this way, the VPS is required to have `Docker` installed.**

1. Natively, we could create a VPS as above, and then install Docker on it.

   * Create a VPS as above

     ...

   * Install Docker on it

     Check out the corresponding official documentation, e.g., For Ubuntu, https://docs.docker.com/install/linux/docker-ce/ubuntu/

   * We already set up the project so that Nginx runs in its own container, and the Flask application and Gunicorn run in another container.

     ```bash
     # Build the images
     $ docker-compose build
     
     # Run the containers
     $ docker-compose up
     ```

2. Quicker way: `docker-machine`

   * Manage "Dockerized hosts" ("machines"), which are virtual hosts installed with Docker Engine, that run in a cloud
   * Simply run Docker containers on a "machine"

   See the section below.

<br>

***

#### `docker-machine` to manage "Dockerized hosts" ("machines"), which are virtual hosts installed with Docker Engine, that run in a cloud

***

Cloud available choices:

* **Amazon EC2**
* Azure
* Linode
* DigitalOcean
* ...

***

Follow the instructions on https://docs.docker.com/machine/drivers/aws/ and https://docs.docker.com/machine/examples/aws/

* Create an AWS IAM user `flask-blog-user` for the application, with `AmazonEC2FullAccess`.

* Put the credentials in an AWS configuration file

  ```bash
  $ mkdir ~/.aws/
  $ cd ~/.aws
  $ touch credentials
  ```

  Write the following:

  ```
  [default]
  aws_access_key_id = ...
  aws_secret_access_key = ...
  aws_vpc_id = ...
  ```

* Use `docker-machine` to create an AWS EC2 instance, and install Docker Engine on it

  ```bash
  $ docker-machine create --driver amazonec2 --amazonec2-region ap-northeast-2 --amazonec2-open-port 8000 "flask-blog-machine"
  ```

  Make the newly created machine active, i.e., connecting to that newly created machine

  ```bash
  $ eval $(docker-machine env flask-blog-machine)
  
  # Check it out
  $ docker-machine active
  flask-blog-machine
  ```

  Check out the IP address of the machine

  ```bash
  $ docker-machine ip flask-blog-machine
  ```

* Since we've connected to the machine, we can run Docker container on that machine

***

How to make `docker-compose` and `docker-machine` work together?

To be continued...

***