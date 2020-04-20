from flask import Flask
from flask_migrate import Migrate

import db_schema

# App config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/test_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database
db_schema.db.init_app(app)
migrate = Migrate(app, db_schema.db)
