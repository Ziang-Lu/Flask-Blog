# Deployment Options

## Fundamentals: VPS + Web Server + Python Web App WSGI Server

#### VPS Hosting Options

* AWS EC2
* Azure
* **Linode**
* Heroku
* DigitalOcean
* InMotion
* Bluehost
* Hostgator

<br>

#### Web Server Options:

* **Nginx**

<br>

#### Python Web App WSGI Server Options:

* **Gunicorn**

  ***

  **How to setup Gunicorn for handling concurrent requests?**

  In Gunicorn, a worker corresponds to a process, which has one Python application in it.

  According to https://medium.com/building-the-system/gunicorn-3-means-of-concurrency-efbb547674b7, basically there are three ways to setup Gunicorn for concurrency, which in fact corresponds to the three ways to achieve concurrency in Python:

  * Multiple workers (processes)

    Worker type: `sync`

    ```bash
    # 4 cores
    $ gunicorn --worker=9 "flask_blog:create_app()"  # 9 workers
    
    # Maximum concurrent requests = # of workers
    
    # How to optimize for that?
    # Usually let that be (2 x # of CPUs + 1)
    # => In this case, we set -w to be (2 x 4 + 1 = 9)
    ```

  * Multiple threads

    Worker type: `gthread`

    ```bash
    # 4 core
    $ gunicorn --worker=3 --worker-class=gthread --threads=3 "flask_blog:create_app()"
    
    # Maximum concurrent requests = # of workers x # of threads per worker
    
    # => In this case, we simply choose -w to be 3 and --threads to be 3
    ```

  * **Aynchronous workers** (Recommended for IO-bound applications)

    Worker type: `gevent`

    ```bash
    # 4 cores
    $ gunicorn --worker=9 --worker-class=gevent --worker-connections=1000 "flask_blog:create_app()"
    
    # Maximum concurrent requests = # of workers x # of worker connections
    
    # => In this case, we still simply choose -w to be (2 x 4 + 1 = 9)
    ```

  ***

* Waitress

* uWSGI

***

How do **Nginx** and **Gunicorn** work together?

* Nginx handles static information (like CSS files, JavaScript codes, pictures, etc.)
* Gunicorn runs on the host and listens on port 8000.
* Nginx forwards Flask requests to Gunicorn, and let Gunicorn handle Flask requests

***

<br>

## Dockerization: Linux Server + Web Server (in `Docker` Container) + Python Web App WSGI Server (in `Docker` Container)

**=> In this way, the VPS is required to have `Docker` installed.**

<img src="https://github.com/Ziang-Lu/Flask-Blog/blob/master/Flask-Blog%20Deployment.png?raw=true">

1. Natively, we could create a VPS as above, and then install Docker on it.

   * Create a VPS

   * Install Docker on it

     Check out the corresponding official documentation, e.g., For Ubuntu, https://docs.docker.com/install/linux/docker-ce/ubuntu/

   * Run the Dockerized application:

     ```shell
  # Use docker-compose to...
     
     # Build the service images
     $ docker-compose build
     
     # Run the services (containers)
     $ docker-compose up
     ```

2. Quicker way: `docker-machine` tool, released by Docker officials

   -> Manage "Dockerized hosts" ("machines"), which are virtual hosts installed with Docker Engine, that run in a cloud

     *(Essentially, this combines the first two steps in the above approach.)*

   * Simply run the Dockerized application () on a "machine"

   -> See the section below

***

#### `docker-machine` to manage "Dockerized hosts" ("machines"), which are virtual hosts installed with Docker Engine, that run in a cloud

Cloud available choices:

* **Amazon EC2**
* Azure
* Linode
* DigitalOcean
* ...

Follow the instructions on https://docs.docker.com/machine/drivers/aws/ and https://docs.docker.com/machine/examples/aws/

* Create an AWS IAM user `flask-blog-user` for the application, with `AmazonEC2FullAccess`

* Configure AWS user-related environment variables

  ```bash
  export AWS_ACCESS_KEY_ID=...
  export AWS_SECRET_ACCESS_KEY=...
  export AWS_VPC_ID=...
  ```

* Use `docker-machine` to create an AWS EC2 instance, with Docker Engine installed on it

  ```bash
  $ docker-machine create --driver amazonec2 --amazonec2-region ap-northeast-2 --amazonec2-open-port 80 "flask-blog-machine"
  ```

* Make the newly created machine active, i.e., connecting to that newly created machine

  ```bash
  $ eval $(docker-machine env flask-blog-machine)
  
  # Check it out
  $ docker-machine active
  flask-blog-machine
  ```
  
* Check out the IP address of the machine

  ```bash
  $ docker-machine ip flask-blog-machine
  ```
  
* Since we've connected to the machine, we can run Docker container on that machine.

  ```bash
  # Use docker-compose to...
  
  # Build the service images
  $ docker-compose build
  
  # Run the services (containers)
  $ docker-compose up
  ```
  
* To switch back to local Docker host

  ```bash
  $ eval $(docker-machine env -u)
  ```

***

<br>

## Advanced: Same Setup as 2, but Deployed to Cluster in Cloud (Deploy到集群)

So far, we've been deploying to a single machine in a cloud. But what if we want to **deploy to a cluster in a cloud**?

Basically, there are two ways: `docker-swarm` and `Kubernetes`. Detailed to be filled in the future...

