# Code References:
  # API Testing serie: https://www.linkedin.com/learning/api-testing-foundations/next-steps
  # API Testing: http://katrinatester.blogspot.com/2015/09/api-web-services-microservices-testing.html
  # Swagger docs: https://swagger.io/docs/specification/about/
  # Postman docs: https://learning.postman.com/docs/postman/api-documentation/documenting-your-api/
  # Flask API docs: https://tedboy.github.io/flask/generated/generated/flask.Request.get_json.html
  # Udacity Student HUB
    # User https://github.com/paulakedouk/triviaapi
    # User https://github.com/dharmykoya/triviaapi
    # User https://github.com/IvanCanales/TriviaAPI
    # User https://github.com/lucasauman/triviaAPI
    # User https://github.com/samuel-js/Trivia-Api
  # Tree : https://rschu.me/list-a-directory-with-tree-command-on-mac-os-x-3b2d4c4a4827

# ------------------------------------------------------------- #
# Imports 
# ------------------------------------------------------------- #
import os
from flask import Flask, request, abort, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
from models import setup_db, Question, Category

# Global function for pagination.
def paginate_items(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * 10 # ITEMS_PER_PAGE = 10
  end = start + 10
  formatted = [i.format() for i in selection]

  if(len(formatted) < start):
      abort(404)

  return formatted[start:end]

# ------------------------------------------------------------- #
# APP configuraration 
# ------------------------------------------------------------- #

def create_app(test_config=None):
  app = Flask(__name__, instance_relative_config=True)
  # Cors app
  setup_db(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  @app.route('/')
  @cross_origin()
  def test():
      
    return "Hey!"

  # ------------------------------------------------------------- #
  # Application Enpoints
  # ------------------------------------------------------------- #

  # Return all categories available
  @app.route('/categories')
  def return_categories():
    get_categories = Category.query.order_by(Category.id).all()
    categories_dict = {}

    try:

      for category in get_categories:
        categories_dict[category.id] = category.type

      return jsonify({
        'success': True,
        'categories': categories_dict,
        'all_categories': len(categories_dict)
      })

    except:
      abort(422)

  # Return questions based on category 
  @app.route('/categories/<int:id>/questions')
  def return_questions_by_category(id):
    questions = Question.query.filter_by(category=id).all()
    current_questions = paginate_items(request, questions)

    formatted_questions = [question.format() for question in questions]
    category = Category.query.filter_by(id=id).all()

    if category is None:
      error = 404

    try:
      return jsonify({
        'success':True,
        'questions':current_questions,
        'total_questions':len(formatted_questions),
        'current_category':category[0].type
      })

    except:
      abort(404)

  # Returning Question with pagination=10 
  @app.route('/questions')
  def return_questions():
    questions = Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.id).all()
    
    categories_dict = {}
    
    try:

      for category in categories:
        categories_dict[category.id] = category.type
      
      return jsonify({
        'questions': paginate_items(request, questions),
        'total_questions': len(questions),
        'categories': categories_dict,
        'current_category': None
      })

    except:
      abort(422)

  # Adding new question 
  @app.route('/questions/add', methods=['POST'])
  def add_question():
    body = request.get_json()
    questions = Question.query.order_by(Question.id).all()

    try:

      get_question = body.get('question', None)
      get_answer = body.get('answer', None)
      get_difficulty = body.get('difficulty', None)
      get_category = body.get('category', None)
      
      question = Question(question=get_question, answer=get_answer,
                 difficulty=get_difficulty, category=get_category,)
      
      question.insert()

      return jsonify({
        'success': True,
        'question_id': question.id,
        'questions': paginate_items(request, questions),
        'total_questions': len(questions)
      })

    except:
      abort(422)

  # Deleting a question using id 
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter_by(id=question_id).one_or_none()

    if question is None:
      abort(404)

    try:
      question.delete()

      return jsonify({
        'success': True,
        'deleted_id': question_id
      })

    except:
      abort(422)



  # Searching Questions 
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    search_term = request.get_json()['searchTerm']
    questions = Question.query.all()
    question_array = []

    for i in questions:
      if search_term.lower() in i.question.lower():
        question_array.append(i)
    
    f_questions = [i.format() for i in question_array]

    return jsonify({
      'success':True,
      'questions':f_questions,
      'total_questions':len(question_array),
      'current_category':'None'
    })



  # Return questions for playing quiz
  @app.route('/play', methods=['POST'])
  def play_quiz():
    previous_questions = request.get_json()['previous_questions']
    quiz_category = request.get_json()['quiz_category']['id']
    questions = None

    if quiz_category is 0:
      questions = Question.query.all()
    else:  
      questions = Question.query.filter_by(category=str(quiz_category))

    present_question = ''

    for i in questions:
      if i.id not in previous_questions:
        present_question = i.format()
        break

    return jsonify({
      'success':True,
      'question':present_question,
    })

  # ------------------------------------------------------------- #
  # Error handlers for all expected errors 
  # ------------------------------------------------------------- #

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(405)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "method not allowed"
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422


  return app

    