import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        #self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgres://{}@{}/{}".format('postgres:root','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    


    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_show_category(self):
        """Test _____________ """
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['num_of_results'])
        self.assertTrue(len(data['results']))

    def test_show_category_error(self):
        """Test _____________ """
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],'resource not found')

    def test_show_questions(self):
        """Test _____________ """
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_add_question(self):
        """Test _____________ """
        res = self.client().post('/questions/add')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['added'])
        self.assertTrue(data['num_of_results'])
        self.assertTrue(len(data['results']))

    def test_search_question(self):
        """Test _____________ """
        res = self.client().post('/questions/search')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['num_of_results'])
        self.assertTrue(len(data['results']))

    def test_show_categories(self):
        """Test _____________ """
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['num_of_results'])
        self.assertTrue(len(data['results']))

    def test_show_quiz(self):
        """Test _____________ """
        res = self.client().post('/quiz')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['results']))

    def test_delete_question(self):
        res = self.client().delete('/questions/15')
        question = Question.query.filter(Question.id==15).one_or_none()
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], 15)
        self.assertTrue(data['num_of_results'])
        self.assertTrue(len(data['results']))
        self.assertEqual(question,None) 

    def test_delete_question_error(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],500)
        self.assertEqual(data['message'],'Internal Server Error')
    
    def tearDown(self):
        """Executed after reach test"""
        db.session.rollback()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()