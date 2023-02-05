from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import logging

app = Flask(__name__ , static_url_path='', static_folder='../../static/build' , template_folder='../../static/build')

# backend\backend-master\static\build\index.html

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "345678456789a234567834567892345678934567"
jwt = JWTManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projet.sqlite3'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
logging.basicConfig(level=logging.DEBUG)


# Entity Users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100),  unique=True)
    password = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.String(100), nullable=False)
    profile = db.Column(db.Text, nullable=True)
    date_of_birth = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(100), nullable=True)
    image = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=True)
    Modules = db.relationship('Module', backref='user', lazy=True)
    Evaluations = db.relationship('Evaluation', backref='user', lazy=True)
    ResutatEvaluations = db.relationship('ResutatEvaluation', backref='user', lazy=True)
    def __str__(self):
        return f'{self.id}, {self.firstname},{self.lastname},{self.email},{self.date_created},{self.profile}'  


# Entity cour
class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    cours = db.relationship('Cour', backref='Module', lazy=True)
    def __str__(self):
        return f'{self.id}, {self.title},{self.description},{self.date_created},{self.user_id}'  


# Entity cour
class Cour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.String(100), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'),nullable=False)
    cours = db.relationship('Evaluation', backref='Cour', lazy=True)


# Entity Evaluation
class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    date_created = db.Column(db.String(100), nullable=False)
    cours_id = db.Column(db.Integer, db.ForeignKey('cour.id'),nullable=False)
    Questions = db.relationship('Question', backref='evaluation')
    ResutatEvaluations = db.relationship('ResutatEvaluation', backref='evaluation')


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    propo1 = db.Column(db.Text, nullable=True)
    propo2 = db.Column(db.Text, nullable=True)
    propo3 = db.Column(db.Text, nullable=True)
    file = db.Column(db.Text, nullable=True)
    reponse = db.Column(db.Text, nullable=False)
    valider = db.Column(db.Integer, nullable=False)
    duree = db.Column(db.Integer, nullable=False)
    Niveau = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.String(100), nullable=False)
    evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluation.id'),nullable=False)


class ResutatEvaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluation.id'),nullable=False)
    date_created = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()
