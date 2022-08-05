from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class people(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(20), unique=False, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=False)
    mass = db.Column(db.Integer, unique=False, nullable=False)
    eye_color = db.Column(db.String(30), unique=False, nullable=False)
    skin_color = db.Column(db.String(30), unique=False, nullable=False)
    hair_color = db.Column(db.String(30), unique=False, nullable=False)
    birth_year=db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<people %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender":self.gender,
            "description":self.description
            
        }