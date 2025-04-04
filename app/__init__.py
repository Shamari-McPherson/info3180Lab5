from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import os


app = Flask(__name__)
app.config.from_object(Config)


# Configuration
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a real secret key
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder to store uploaded files

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)


from . import models 
from app import views