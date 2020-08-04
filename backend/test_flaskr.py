import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """Test cases start from here"""

    def setUp(self):
        """Defining variables and starting app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'radesh619','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    # TODO
    # Write at least one test for each test for successful operation and for expected errors.   

    def test_return_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_return_invalid_category_id(self):
        res = self.client().get('/categories/19887/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_return_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10)

    def test_return_questions_failure_case(self):
        res = self.client().get('/quesion')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False) 
        self.assertEqual(data['message'], 'resource not found') 

    #After runnning scripts We have to chane id manually or else it show F
    def test_delete_question(self):
        res = self.client().delete('/questions/2') 
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 2)
                     
    def test_delete_question_error_404(self):      
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_question_error_405(self):
        res = self.client().post('/questions', 
        json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_create_question(self):
        res = self.client().post('/questions/add', 
        json={'question':'TestQuestion', 
              'answer':'TestAnswer', 
              'category':'5', 
              'difficulty':5})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_question_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_question_by_category_error_404(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_search_questions(self):
        request_data = {'searchTerm': 'largest lake in Africa',}
        res = self.client().post('/questions/search', json=request_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)
    
    def test_search_fail_case(self):
        request_data = {'searchTerm': 'dfjdtrergrdgrdgdrg',}
        res = self.client().post('/questions/search', json=request_data)
        data = json.loads(res.data)
        self.assertNotEqual(res.status_code, 404)
        self.assertNotEqual(data['success'], False)

    def test_play_quiz(self):
        request_data = {
            'previous_questions': [5, 9],
            'quiz_category': {
                'type': 'History',
                'id': 4
            }
            }
        res = self.client().post('/play', json=request_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    
    def test_play_quiz_fail_case(self):
        request_data = {
            'previous_questions': [5, 9],
            'quiz_category': {
                'type': 'History',
                'id': 4
            }
            }
        res = self.client().post('/play', json=request_data)
        data = json.loads(res.data)
        self.assertNotEqual(res.status_code, 404)
        self.assertNotEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()