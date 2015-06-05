# coding: utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from alchemydumps import AlchemyDumps, AlchemyDumpsCommand

# create a Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
manager = Manager(app)
alchemydumps = AlchemyDumps(app, db, basedir='tests/')
manager.add_command('alchemydumps', AlchemyDumpsCommand)


# create models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(140), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    content = db.Column(db.UnicodeText)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# run
if __name__ == '__main__':
    manager.run()
