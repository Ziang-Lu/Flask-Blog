# OAuth2 Authorization and OpenID Connect Authentication

The following materials are summarized from this SUPER AWESOME video: https://www.youtube.com/watch?v=996OiexHze0, and all the images credit to the origninal author, i.e., the speaker of the talk.

<br>

## OAuth2 - Authorization

OAuth2 solves **authorization** problem.

=> <u>How do a user ("resource owner") to authorize a third-party application ("client"), to grant the application the access to his/her protected resources on an OAuth provider (like Google, Facebook, GitHub, Twitter, etc.)?</u>

=> Thus, it focuses on the problem that <u>third-party application ("client") is trying to access some user-protected API, and how do the user ("resource owner") grant that permission</u>.

<br>

According to the how OAuth 2.0 actually works, there are some workflows:

<img src="https://github.com/Ziang-Lu/Flask-Blog/blob/master/OAuth2%20and%20OpenID%20Connect/Workflows.png?raw=true">

***

* Back channel
  * Communication between servers
  * Secure
  * Indicated as dashed lines in the below diagrams
* Front channel
  * Communication involving the browser
  * Not-so-secure
  * Indicated as solid lines ...

***

<br>

#### Authorization Code Flow

<img src="https://github.com/Ziang-Lu/Flask-Blog/blob/master/OAuth2%20and%20OpenID%20Connect/OAuth2-Authorization%20Code%20Flow.png?raw=true">

<br>

#### Implicit Flow

Only difference from authorization code flow:

* <u>No authorization code involved</u>

  * No exchange of an authorization code for an access token

    => An access token is directly handed back from authorization server

<img src="https://github.com/Ziang-Lu/Flask-Blog/blob/master/OAuth2%20and%20OpenID%20Connect/OAuth2-Implicit%20Flow.png?raw=true">

<br>

## OpenID Connect - Authentication

OpenID Connect is just a <u>thin wrapper around OAuth 2.0</u>, to **also handle authentication** problem.

=> Thus, it focuses on the problem that <u>a user decides to log-in to a third-party application ("client") through an OAuth provider (like Google, etc.), and how does the application ("client") know about the user information ("protected resources") from that OAuth provider.</u>

<br>

#### Authorization Code Flow for OpenID Connect

Main difference from authorization code flow for OAuth 2.0:

* <u>Newly added scope `openid`</u>
* <u>Newly received `id_token` on server-side, which contains the basic information about the user</u>
* In order to get more information about the user:
  * Either add more detailed scopes in the very beginning
  * Or on server-side, use the access token to fetch more information about the user

<img src="https://github.com/Ziang-Lu/Flask-Blog/blob/master/OAuth2%20and%20OpenID%20Connect/OpenID%20Connect-Authorization%20Code%20Flow.png?raw=true">

<br>

#### Implicit Flow for OpenID Connect

Authorization Code Flow for OpenID Connect  =>  Implicit Flow for OpenID Connect

=

Authorization Code Flow for OAuth 2  =>  Implicit Flow for OAuth 2

