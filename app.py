"""Demo for OpenID Connect login."""
import logging
import os

import flask
from keycloak import KeycloakOpenID

app = flask.Flask(__name__)  # pylint: disable=invalid-name

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

keycloak_openid = KeycloakOpenID(server_url=os.environ.get("SERVER_URL"),
                                 client_id=os.environ.get("CLIENT_ID"),
                                 realm_name=os.environ.get("REALM_NAME"),
                                 client_secret_key=os.environ.get("CLIENT_SECRET"),)


@app.route("/")
def render_home():
    """List available entries."""
    return flask.render_template("base.html", user_info=flask.session.get("user_info"))


@app.route("/login")
def oidc_login():
    """Perform a login using OpenID Connect."""
    redirect_uri = flask.url_for("oidc_authorize",
                                 _external=True)
    return flask.redirect(keycloak.auth_url(redirect_uri))


@app.route("/login/authorize")
def oidc_authorize():
    """Authorize a login using OpenID Connect (e.g. Elixir AAI)."""
    flask.current_app.logger.info(dict(flask.request.args))
    flask.current_app.logger.info(flask.request.data)
    return flask.redirect("/")


@app.route("/logout")
def oidc_logout():
    """Log out from the oidc session"""
    flask.session.clear()
    logout_url = os.environ.get("LOGOUT_URL")
    if logout_url:
        redirect_uri = flask.url_for("render_home",
                                     _external=True)

        return flask.redirect(f"{logout_url}?redirect_uri={redirect_uri}")
    return flask.redirect(redirect_uri)


@app.route("/external-logout", methods=["GET", "POST"])
def oidc_external_logout():
    """Log out from the oidc session"""
    flask.current_app.logger.info(dict(flask.request.args))
    flask.current_app.logger.info(flask.request.data)
    flask.session.clear()
    return flask.jsonify(flask.request.json)


if __name__ != '__main__':
    # assume the container is running in gunicorn
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
