# Demonstration of OpenID Connect

A flask app that uses OpenID Connect for login.

## Setup:

You need to set the environment variables `CLIENT_SECRET`, `CLIENT_ID`, and `SERVER_METADATA_URL`.

### To use Google for login:

Set up a project and OAUTH login at https://console.cloud.google.com/projectselector2/apis/.

The variables should be similar to:
```
CLIENT_ID = 123456789012-abc1def2ghi3jkl4mno5pqr6stu7vwx8.apps.googleusercontent.com
CLIENT_SECRET = aBcDeFgHiJkLmNoPqRsTuVxY
SERVER_METADATA_URL = https://accounts.google.com/.well-known/openid-configuration
```

### Keycloak example:

```
CLIENT_SECRET = aBcDeFgHiJkLmNoPqRsTuVxYz0123456
CLIENT_ID = oidc-demo
SERVER_METADATA_URL = https://sso.dckube.scilifelab.se/realms/data-tracker/.well-known/openid-configuration
```

## Code explanation

### Activate the Oauth login

The example uses the Authlib Flask integration (`pip install authlib`) for its simplicity. There are many other other modules that can be used instead.

Documentation for the Authlib Flask integration: https://docs.authlib.org/en/latest/client/flask.html

```
oauth.register("oidc_entry",
               client_secret=os.environ.get("CLIENT_SECRET"),
               client_id=os.environ.get("CLIENT_ID"),
               server_metadata_url=os.environ.get("SERVER_METADATA_URL"),
               client_kwargs={"scope": "openid profile email roles"})
```

* `oidc_entry` is the internal reference to the setup. You may add as many different ones as you want.
* `client_id` is the "username"
* `client_secret` is the "password"
* `client_kwargs` will in most cases only define the scopes. The default (and required) ones are `{"scope": "openid profile email"})`

Users log in by accessing the `/login` endpoint:

```
@app.route("/login")
def oidc_login():
    """Perform a login using OpenID Connect."""
    redirect_uri = flask.url_for("oidc_authorize",
                                 _external=True)
    return oauth.oidc_entry.authorize_redirect(redirect_uri)
```

`oauth.oidc_entry.authorize_redirect(redirect_uri)` will redirect the user to the external login provider, as well as define where that provider should redirect the user after login. In this case `/login/authorize`.

```
@app.route("/login/authorize")
def oidc_authorize():
    """Authorize a login using OpenID Connect (e.g. Elixir AAI)."""
    token = oauth.oidc_entry.authorize_access_token()
    flask.session["user_info"] = token["userinfo"]
    return flask.redirect("/")
```

The `token` will contain e.g. hashes, nonces, and the user information provided by the login provider. It includes e.g. email, the providers id for the user, and many other things.
