import os
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///capital.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]

from routes import *

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)