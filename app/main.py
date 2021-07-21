import os
from flask import Flask, request, abort, jsonify, abort
from flask.globals import session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import defer
from flask_cors import CORS
import random
from models import setup_db, Question, Category, db

app = Flask(__name__)
setup_db(app)

CORS(app)

QUESTIONS_PER_PAGE = 10

#def create_app(test_config=None):
  # create and configure the app

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

@app.route('/')
#@cross_origin()
def hello():
  return jsonify({"message":"Hello World!"})



'''
@TODO: 
Create an endpoint to handle GET requests 
for all available categories.
'''
@app.route('/categories', methods=['GET'])
def show_categories():
  categories = Category.query.all()
  formatted_categories = [category.format() for category in categories]
  
  return jsonify({
      'success':True,
      'results':formatted_categories,
      'num_of_results':len(formatted_categories)
      })

'''
@TODO: 
Create an endpoint to handle GET requests for questions, 
including pagination (every 10 questions). 
This endpoint should return a list of questions, 
number of total questions, current category, categories. 

TEST: At this point, when you start the application
you should see questions and categories generated,
ten questions per page and pagination at the bottom of the screen for three pages.
Clicking on the page numbers should update the questions. 
'''
@app.route('/questions', methods=['GET'])
def show_questions():
  page = request.args.get('page',1,type=int)
  start = (page-1)*10
  end = start + 10
  questions = Question.query.all()
  categories = Category.query.all()
  formatted_questions = [question.format() for question in questions]
  formatted_categories = [category.format() for category in categories]


  
  return jsonify({
      'success':True
      ,'questions':formatted_questions[start:end]
      ,'total_questions':len(questions)
      ,'categories':formatted_categories
  })


  
'''
@TODO: 
Create an endpoint to DELETE question using a question ID. 

TEST: When you click the trash icon next to a question, the question will be removed.
This removal will persist in the database and when you refresh the page. 
'''
@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
  try:
    Question.query.get(question_id).delete()
    db.session.commit()
    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]
  except:
    abort(500)

  return jsonify({
    'success':True,
    'deleted':question_id,
    'results':formatted_questions,
    'num_of_results':len(formatted_questions)
  })  
'''
@TODO: 
Create an endpoint to POST a new question, 
which will require the question and answer text, 
category, and difficulty score.

TEST: When you submit a question on the "Add" tab, 
the form will clear and the question will appear at the end of the last page
of the questions list in the "List" tab.  
'''
@app.route('/questions/add', methods=['POST'])
def insert_question():
  try:
    question = request.get_json()['question']
    answer = request.get_json()['answer']
    difficulty = request.get_json()['difficulty']
    category = int(request.get_json()['category'])
    category = category + 1
    new_question = Question(question=question,category=category,difficulty=difficulty,answer=answer)
    new_question.insert()
    id = new_question.id
    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]
  except:
    abort(500)

  return jsonify({
    'success':True,
    'added':id,
    'results':formatted_questions,
    'num_of_results':len(formatted_questions)
  }) 
'''
@TODO: 
Create a POST endpoint to get questions based on a search term. 
It should return any questions for whom the search term 
is a substring of the question. 

TEST: Search by any phrase. The questions list will update to include 
only question that include that string within their question. 
Try using the word "title" to start. 
'''
@app.route('/questions/search', methods=['POST'])
def search_question():
  search_term = request.get_json()['searchTerm']
  questions = Question.query.filter(Question.question.like('%'+search_term+'%')).all()
  formatted_questions = [question.format() for question in questions]
  if len(questions) == 0:
    abort(404)
  else:
    return jsonify({
        'success':True,
        'results':formatted_questions,
        'num_of_results':len(formatted_questions)
        })
'''
@TODO: 
Create a GET endpoint to get questions based on category. 

TEST: In the "List" tab / main screen, clicking on one of the 
categories in the left column will cause only questions of that 
category to be shown. 
'''


@app.route('/categories/<int:category_id>/questions', methods=['GET'])
def show_questions_by_category(category_id):
  category_id = category_id+1
  questions = Question.query.filter_by(category=category_id).all()
  formatted_questions = [question.format() for question in questions]
  if len(questions) == 0:
    abort(404)
  else:
    return jsonify({
        'success':True,
        'results':formatted_questions,
        'num_of_results':len(formatted_questions),
        'current_category':category_id
        })

'''
@TODO: 
Create a POST endpoint to get questions to play the quiz. 
This endpoint should take category and previous question parameters 
and return a random questions within the given category, 
if provided, and that is not one of the previous questions. 

TEST: In the "Play" tab, after a user selects "All" or a category,
one question at a time is displayed, the user is allowed to answer
and shown whether they were correct or not. 
'''
@app.route('/quiz', methods=['POST'])
def show_questions_randomly():

  category = int(request.get_json()['quiz_category']['id']) + 1
  previous_questions = request.get_json()['previous_questions']
  questions = ''
  if category == 11:
    questions = Question.query.all()
  else:
    questions = Question.query.filter_by(category=category).all()
  formatted_questions = [question.format() for question in questions]
  next_question = formatted_questions[random.randint(0,len(formatted_questions)-1)]
  while next_question['id'] in previous_questions:
    next_question = formatted_questions[random.randint(0,len(formatted_questions)-1)] 
  #random = random.sample(formatted_questions,len(formatted_questions))
  if category is None:
    abort(422)
  else:
    return jsonify({
        'success':True,
        'results':next_question
        })


@app.route('/img/<img>', methods=['GET'])
def show_img(img):
  return open('/img/'+img,'r').read()

'''
@TODO: 
Create error handlers for all expected errors 
including 404 and 422. 
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success':False,
        'error':404,
        'message':'resource not found'
    }),404

@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        'success':False,
        'error':422,
        'message':'Unprocessable Entity'
    }),422

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success':False,
        'error':500,
        'message':'Internal Server Error'
    }),500

  #return app

    