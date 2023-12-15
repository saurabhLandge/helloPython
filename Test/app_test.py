import unittest
from app import app


class BasicTestsSetup(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass


class TestCaseExamples(unittest.TestCase):

    def test_home_status(self):
        tester = app.test_client(self)
        response = tester.get('/staff', content_type='html/text')
        self.assertEqual(response.status_code, 200)  # pass (test if the page renders successfully)

    def test_home_content(self):
        tester = app.test_client(self)
        response = tester.get('/staff', content_type='html/text')
        self.assertTrue(b'Id' in response.data)  # passed the test
        # self.assertFalse(b'Admin' in response.data)  # passed the test

    def test_update_page(self):
        tester = app.test_client(self)
        response = tester.get('/update', content_type='html/text')  # to test if update page exists
        self.assertNotEqual(response.status_code, 404)  # pass the test (404 error if no access to the url)
        self.assertIn(b'name', response.data)


if __name__ == '__main__':
    unittest.main()
