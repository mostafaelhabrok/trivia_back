import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

#database_name = "trivia"

database_name = "d5rhp52814u06o"

#database_path = "postgres://{}/{}@{}/{}".format('postgres','root','localhost:5432', database_name)
#database_path = "postgres://{}@{}/{}".format('postgres:root','localhost:5432', database_name)

database_path = "postgres://{}@{}/{}".format('wuzbdtfunffgor:c948db531fee8633094aa79ba54db3f3bde4254c75aad7d1e483a24e187b3dc7','ec2-54-147-93-73.compute-1.amazonaws.com:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Question

'''
class Question(db.Model):  
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  category = Column(String)
  difficulty = Column(Integer)

  def __init__(self, question, answer, category, difficulty):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty
    }

'''
Category

'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)

  def __init__(self, type):
    self.type = type

  """ def format(self):
    return {
      'id': self.id,
      'type': self.type
    } """
  
  def format(self):
    return [ 
      self.type
    ]