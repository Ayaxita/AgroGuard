from App.exts import db
from datetime import datetime

class Testuser(db.Model):
    __tablename__ = 'testuser'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    last_login = db.Column(db.DateTime)
