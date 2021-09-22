from enum import unique
from sqlalchemy.sql.operators import is_distinct_from
from database import db
from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(256), unique = True)
    name = db.Column(db.String(256))

class OAuth(db.Model, OAuthConsumerMixin):
    provider_user_id = db.Column(db.String(256), unique = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)