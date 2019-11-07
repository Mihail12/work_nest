import os
import unittest
from unittest import mock


from app import app


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['BASEDIR'] = os.getcwd()
        self.app = app.test_client()
        self.handle = 'test'

    # executed after each test
    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @mock.patch('requests.get', return_value=mock.Mock(status_code=200))
    @mock.patch('app.get_profile_picture', return_value=['test_url_to_picture', ])
    @mock.patch('app.save_file_to_fs', return_value=200)
    def test_successful_scrape(self, request_get, get_profile_picture, save_file_to_fs):
        response = self.app.post('/scrape/', data={'handle': self.handle}, follow_redirects=True)
        self.assertEqual(response.data.decode('utf-8'), 'successful')
        self.assertEqual(response.status_code, 200)

    @mock.patch('requests.get', return_value=mock.Mock(status_code=404))
    def test_scrape_request_error(self, request_get):
        response = self.app.post('/scrape/', data={'handle': self.handle}, follow_redirects=True)
        self.assertEqual(response.data.decode('utf-8'), f'Twitter has no handle with name: {self.handle}')
        self.assertEqual(response.status_code, 404)

    @mock.patch('requests.get', return_value=mock.Mock(status_code=400))
    def test_scrape_connection_error(self, request_get):
        response = self.app.post('/scrape/', data={'handle': self.handle}, follow_redirects=True)
        self.assertEqual(response.data.decode('utf-8'), 'There is error with connection to twitter')
        self.assertEqual(response.status_code, 400)

    @mock.patch('requests.get', return_value=mock.Mock(status_code=200))
    @mock.patch('app.get_profile_picture', return_value=[])
    def test_scrape_profile_url_error(self, request_get, get_profile_picture):
        response = self.app.post('/scrape/', data={'handle': self.handle}, follow_redirects=True)
        self.assertEqual(response.data.decode('utf-8'), 'There is an issue with scraping profile url')
        self.assertEqual(response.status_code, 500)

    @mock.patch('requests.get', return_value=mock.Mock(status_code=200))
    @mock.patch('app.get_profile_picture', return_value=['test_url_to_picture', ])
    @mock.patch('app.save_file_to_fs', return_value=400)
    def test_scrape_profile_url_error(self, request_get, get_profile_picture, save_file_to_fs):
        response = self.app.post('/scrape/', data={'handle': self.handle}, follow_redirects=True)
        self.assertEqual(response.data.decode('utf-8'), 'There is error while getting image')
        self.assertEqual(response.status_code, 400)

    @mock.patch('os.path.exists', return_value=True)
    def test_get_picture_ok(self, exists):
        response = self.app.get(f'/user/{self.handle}/profile_pic/', follow_redirects=True)
        self.assertIn(f'{self.handle}.jpg', response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)

    @mock.patch('os.path.exists', return_value=False)
    def test_get_picture_404(self, exists):
        response = self.app.get(f'/user/{self.handle}/profile_pic/', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    @mock.patch('os.listdir', return_value=['test.jpg', 'test1.jpg'])
    def test_get_pictures_ok(self, listdir):
        response = self.app.get(f'/users/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode('utf-8')
        self.assertIn('test.jpg', response_text)
        self.assertIn('test1.jpg', response_text)
        self.assertIn('<br>', response_text)

    @mock.patch('os.listdir', return_value=[])
    def test_get_pictures_404(self, listdir):
        response = self.app.get(f'/users/', follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.decode('utf-8'), 'There is no scraped users')


if __name__ == "__main__":
    unittest.main()