from app import app
from database import db
from flask import render_template, redirect, url_for, session
from flask_login import current_user, login_user, logout_user
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
import os

from models import *
from forms import *
from scrape import get_yahoo_articles
from stocks import output_historical

google_blueprint = make_google_blueprint(
    client_id = os.environ['GOOGLE_CLIENT_ID'], 
    client_secret = os.environ['GOOGLE_CLIENT_SECRET'],
    scope = ['https://www.googleapis.com/auth/userinfo.email openid',
           'https://www.googleapis.com/auth/userinfo.profile openid'],
    offline = True,
    reprompt_consent = True,
    storage = SQLAlchemyStorage(OAuth, db.session, user = current_user)
)

app.register_blueprint(google_blueprint)

@app.route('/')
def index():
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    if current_user.is_authenticated and google.authorized:
        google_data = google.get(user_info_endpoint).json()
    return render_template('index.html', google_data = google_data,
        fetch_url = google.base_url + user_info_endpoint)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    resp = blueprint.session.get('/oauth2/v2/userinfo')
    user_info = resp.json()
    user_id = str(user_info['id'])
    oauth = OAuth.query.filter_by(provider = blueprint.name,
                                  provider_user_id = user_id).first()
    if not oauth:
        oauth = OAuth(provider=blueprint.name,
                      provider_user_id=user_id,
                      token=token)
    else:
        oauth.token = token
        db.session.add(oauth)
        db.session.commit()
        login_user(oauth.user)
    if not oauth.user:
        user = User(
            email = user_info["email"],
            name = user_info["name"], 
        )
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()
        login_user(user)
    return False

@app.route('/yahoo')
def yahoo():
    return render_template('yahoo.html', urls = get_yahoo_articles())

@app.route('/historical', methods = ['POST', 'GET'])
def historical():
    form = HistoricalTickerForm()
    if form.validate_on_submit():
        created = output_historical(form.ticker.data)
        if not created:
            return render_template('historical.html', 
                ticker = form.ticker.data, created = not created, form = form)
        else: 
            return redirect('/historical/stock=' + form.ticker.data)
    return render_template('historical.html', form = form)

@app.route('/historical/stock=<ticker>')
def display(ticker):
    return redirect(url_for('static', filename = f'/stocks/{ticker}.html'))