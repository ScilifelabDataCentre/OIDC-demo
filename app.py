"""Demo for OpenID Connect login."""
import logging
import os

import flask

from authlib.integrations.flask_client import OAuth

app = flask.Flask(__name__)  # pylint: disable=invalid-name

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

oauth = OAuth(app)
oauth.register('oidc_entry',
               client_secret=os.environ.get("CLIENT_SECRET"),
               client_id=os.environ.get("CLIENT_ID"),
               server_metadata_url=os.environ.get("SERVER_METADATA_URL"),
               client_kwargs={'scope': 'openid profile email'})

@app.route('/')
def root_page():
    """List available entries."""
    return flask.render_template('base.html')


@app.route('/login/')
def oidc_login():
    """Perform a login using OpenID Connect (e.g. Elixir AAI)."""
    client = oauth.create_client('oidc_entry')
    redirect_uri = flask.url_for('oidc_authorize',
                                 _external=True)
    return client.authorize_redirect(redirect_uri)


@app.route('/login/authorize/')
def oidc_authorize():
    """Authorize a login using OpenID Connect (e.g. Elixir AAI)."""
    client = oauth.create_client('oidc_entry')
    token = client.authorize_access_token()
    if 'id_token' in token:
        user_info = client.parse_id_token(token)
    else:
        user_info = client.userinfo()

    return flask.jsonify(user_info)
