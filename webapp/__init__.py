from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import DebugConfig

app = Flask(__name__)
app.config.from_object(DebugConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from webapp import routes
from webapp import api
from webapp import models
