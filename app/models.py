# Add any model classes for Flask-SQLAlchemy here
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import db


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    poster = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __init__(self, title, description, poster, created_at=None):
        self.title = title
        self.description = description
        self.poster = poster
        if created_at is None:
            self.created_at = datetime.now()
        else:
            self.created_at = created_at
        
    def __repr__(self):
        return f'<Movie {self.title}>'