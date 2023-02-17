from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256))
    msg = db.Column(db.Text)

    def __repr__(self) -> str:
        return self.username

