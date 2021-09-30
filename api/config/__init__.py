from flask import Flask

from sqlalchemy.orm import declarative_base

from config.db import SQLAlchemy
from config.urls import register_urls
from config import settings

app = Flask(__name__)
app.config["DEBUG"] = settings.DEBUG
app.config['DATABASE_URI'] = settings.DATABASE_URI

db = SQLAlchemy()
Base = declarative_base()
db.init_app(app, Base)

register_urls(app)
