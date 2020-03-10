# Flask Blog

This repo contains `Flask-Blog` project, which is a basic blogging application.

Mainly implemented as taught by *Corey Schafer* on his YouTube channel https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=1, but also incooperate RESTful microservices

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

We separate `user_service` and `post_service` out as a Flask-based web services:

* `user_service` is responsible for all the logics and information related to users, and talks to `PostgreSQL` directly.
  
  * The user following system is also implemented in `user_service`, and presented in the main Flask-Blog app.
  
  Defined resources:
  
  * `UserList`
  
    Route: `/users`
  
    | Method | Description                                         | Request Form Schema                                         | Response Status Code                                         |
    | ------ | --------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------ |
    | GET    | Returns the user with a specified username or email | Query:<br>`username`: string<br>`email`: string             | 200 on success, 400 on no username or email privided, 404 on user not found |
    | POST   | Adds a user with the given name, email and password | `username`: string<br>`email`: string<br>`password`: string | 201 on success, 400 on invalid data provided                 |
  
  * `UserItem`
  
    Route: `/users/<int:id>`
  
    | Method | Description                            | Request Form Schema                                          | Response Status Code                         |
    | ------ | -------------------------------------- | ------------------------------------------------------------ | -------------------------------------------- |
    | GET    | Returns the user with the specified ID |                                                              | 200 on success                               |
    | PUT    | Updates the user with the specified ID | `username`: string<br>`email`: string<br>`image_filename`: string | 200 on success, 400 on invalid data provided |
  
  * `UserAuth`
  
    Route: `/user-auth/`
  
    | Method | Description                 | Request Form Schema                                          | Response Status Code                                         |
    | ------ | --------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
    | GET    | Handles user authentication | <u>Query:</u><br/>`email`: string<br/>JSON:<br/>`password`: string | 200 on success, 404 on user not found, 401 on authentication failed |
  
  * `UserFollow`
  
    Route: `/user-follow/<int:follower_id>/<followed_username>`
  
    | Method | Description                                                  | Request Form Schema | Response Status Code                                         |
    | ------ | ------------------------------------------------------------ | ------------------- | ------------------------------------------------------------ |
    | POST   | Lets the given follower follow the user with the given username |                     | 201 on success, 404 on followee not found, 400 on invalid data provided |
    | DELETE | Lets the given follower unfollow the user with the given username |                     | 204 on success, 404 on followee not found, 400 on invalid data provided |
  
* `post_service` is responsible for all the logics and information related to user posts, and talks to `PostgreSQL` directly.

  Defined resources:

  * `PostList`

    Route: `/posts`

    | Method | Description                                      | Request Form Schema                                    | Response Status Code |
    | ------ | ------------------------------------------------ | ------------------------------------------------------ | -------------------- |
    | GET    | Returns all posts (optionally with some filters) | <u>Query</u><br>`user`: string<br>`author`: string     | 200 on success       |
    | POST   | Adds a new post                                  | `user_id`: int<br>`title`: string<br>`content`: string | 201 on success       |

  * `PostItem`

    Route: `/posts/<int:id>`

    | Method | Description                            | Request Form Schema                  | Response Status Code                  |
    | ------ | -------------------------------------- | ------------------------------------ | ------------------------------------- |
    | GET    | Returns the post with the specified ID |                                      | 200 on success, 404 on post not found |
    | POST   | Updates the post with the specified ID | `title`: string<br>`content`: string | 200 on success                        |
    | DELETE | Deletes the post with the specified ID |                                      | 204 on success                        |

  * `PostLike`

    Route: `/posts/<int:post_id>/likes`

    | Method | Description          | Request Form Schema | Response Status Code                  |
    | ------ | -------------------- | ------------------- | ------------------------------------- |
    | POST   | Likes the given post |                     | 201 on success, 404 on post not found |

  * `PostComment`

    Route: `posts/<int:post_id>/comments`

    | Method | Description                | Request Form Schema              | Response Status Code                  |
    | ------ | -------------------------- | -------------------------------- | ------------------------------------- |
    | POST   | Comments on the given post | `user_id`: int<br>`text`: string | 201 on success, 404 on post not found |

* `Marshmallow/Flask-Marshmallow` is used for schema definition & deserialization (including validation) / serialization.

* Since these web services are backed by `PostgreSQL` database, `Flask-SQLAlchemy` module is used for ORM-related tasks.

The communication between the main Flask-Blog app and the web services is through RESTful API, via `JSON`.

<br>

In this way, the original Flask-Blog app now becomes a "skeleton" or a "gateway", which talks to `user_service` and `post_service`, uses the fetched data to render HTML templates.

* The main Flask-Blog app uses `WTForms` and `Flask-WTF` to implement forms.

* *REST架构中要求client-server的communication应该是"无状态"的, 即一个request中必须包含server (service)处理该request的全部信息, 而在server-side不应保存任何与client-side有关的信息, 即server-side不应保存任何与某个client-side关联的session.*

  *=> 然而, 我们应该区分"resource state"和"application state": REST要求的无状态应该是对resource的处理无状态, 然而在main application本身里面我们需要保存应用状态, 即user的login和session等.*

  Thus, in the original Flask-Blog app, we still use `Flask-Login` to handle user log-in/log-out and authentication issues, as well as session management.
  
  ***
  
  In the original Flask-Blog app, we also provide OpenID Connect authentication options, from either Google or GitHub, to sign-in and log-in to the app.
  
  ***
  
  For a **general, high-level introduction to OAuth 2.0 authorization and OpenID Connect authentication, as well as different workflows**, check out this note:
  
  https://github.com/Ziang-Lu/Flask-Blog/blob/master/OAuth2%20and%20OpenID%20Connect/OAuth2%20Authorization%20and%20OpenID%20Connect%20Authentication.md
  
  ***
  
  * <u>Google Sign-In</u>
  
    Google Sign-In workflow in my Flask-Blog app:
  
    *(Essentially, this is an <u>Implicit Flow for OpenID Connect</u>.)*
  
    <img src="https://github.com/Ziang-Lu/Flask-Blog/blob/master/Google%20Sign-In%20Flow.png?raw=true">
    
    * Front-end implementation according to https://developers.google.com/identity/sign-in/web/sign-in
    * Back-end implementation according to https://developers.google.com/identity/sign-in/web/backend-auth
    
  * <u>GitHub Sign-In</u>
  
  ***

<br>

### Additional Features

* As a presentation of the user following system, a logged-in user is able to choose to show only the posts authored by himself and the followed users.

* Asynchronous tasks:

  *Some actions in the app takes long time to run, which blocks the server to handle the request.*

  Thus, `Celery` is used as an asynchronous task queue (with `Redis` as the broker (message queue)) to handle those long-running tasks, like sending email to users.

<br>

## License

This repo is distributed under the <a href="https://github.com/Ziang-Lu/Flask-Blog/blob/master/LICENSE">MIT license</a>.

