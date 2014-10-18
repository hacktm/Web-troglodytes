import os
import StringIO

import mock

from django import test
from django.core import files
from django.contrib.auth.models import User

from . import models
from . import transform



class TestPhoto(test.TestCase):
    def setUp(self):
        self.client = test.client.Client()
        self.user = User.objects.create_user('joe', 'joe@google.com', 'joepwd')
    # def test_upload(self):
    #     title = 'kittey.jpg'
    #     photo = models.Photo.objects.create(title=title)
    #     photo.upload_local_image(title, '/home/stz/Pictures/kittey.jpg')
    #     self.assertIsNotNone(photo.image)

    
    # @mock.patch('exifread.process_file', new_callable=StringIO.StringIO())
    # def test_transform(self, mock_output):
        # instance = MockClass.return_value
        # instance.method.return_value = 'foo'
        # assert Class() is instance
        # assert Class().method() == 'foo'
        # pass
        # tags = transform.get_location('this wont matter')

    def test_put_photo(self):
        data = {
            'title': 'spoon',
            'description': 'There is no spoon',
            'image': open('/home/flavius/Pictures/hacktm_photo.jpg', 'rb'),
        }
        import ipdb; ipdb.set_trace()
        response = self.client.post(
            'http://127.0.0.1:8000/api/photo/',
            data,
        )

        return response
