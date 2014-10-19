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
        response = self.client.post(
            'http://127.0.0.1:8000/api/photo/',
            data,
        )

        return response


    def test_no_gps_exif(self):
        tags = {}
        tags['some_key'] = 'some_text'
        gps_lat, gps_long, gps_alt = transform.get_gps_coordinates(tags)
        self.assertIsNone(gps_lat, 'gps_lat should be none')
        self.assertIsNone(gps_long, 'gps_long should be none')
        self.assertIsNone(gps_alt, 'gps_alt should be none')

        tags['GPS GPSLatitude'] = '[45, 10, 34/100]'
        gps_lat, gps_long, gps_alt = transform.get_gps_coordinates(tags)
        self.assertIsNotNone(gps_lat, 'gps_lat should not be none')
        self.assertIsNone(gps_long, 'gps_long shoud be none')
        self.assertIsNone(gps_alt, 'gps_alt should be none')

        tags['GPS GPSLongitude'] = '[25, 8, 5432/100]'
        gps_lat, gps_long, gps_alt = transform.get_gps_coordinates(tags)
        self.assertIsNotNone(gps_lat, 'gps_lat should not be none')
        self.assertIsNotNone(gps_long, 'gps_long should not be none')
        self.assertIsNone(gps_alt, 'gps_lat, should be none')

        tags['GPS GPSAltitude'] = '8000/226'
        gps_lat, gps_long, gps_alt = transform.get_gps_coordinates(tags)
        self.assertIsNotNone(gps_lat, 'gps_lat should not be none')
        self.assertIsNotNone(gps_long, 'gps_long should not be none')
        self.assertIsNotNone(gps_alt, 'gps_alt should not be none')


    def test_wrong_format_gps_exif(self):
        tags = {}
        tags['GPS GPSLatitude'] = '[d45, 10, 34/100]'
        tags['GPS GPSLongitude'] = '[25, 8, 5432/100]'
        tags['GPS GPSAltitude'] = '8000/226'

        gps_lat, gps_long, gps_alt = transform.get_gps_coordinates(tags)
        self.assertIsNone(gps_lat, 'gps_lat should be none')
        self.assertIsNotNone(gps_long, 'gps_long should not be none')
        self.assertIsNotNone(gps_alt, 'gps_alt should not be none')

        tags['GPS GPSLatitude'] = '[45, 10, 34/100]'
        tags['GPS GPSLongitude'] = '[25, 8, 5432/10d0]'
        gps_lat, gps_long, gps_alt = transform.get_gps_coordinates(tags)
        self.assertIsNotNone(gps_lat, 'gps_lat should not be none')
        self.assertIsNone(gps_long, 'gps_long should be none')
        self.assertIsNotNone(gps_alt, 'gps_alt should not be none')

        tags['GPS GPSLongitude'] = '[25, 8, 5432/100]'
        tags['GPS GPSAltitude'] = '8000x/226'
        gps_lat, gps_long, gps_alt = transform.get_gps_coordinates(tags)
        self.assertIsNotNone(gps_lat, 'gps_lat should not be none')
        self.assertIsNotNone(gps_long, 'gps_long should not be none')
        self.assertIsNone(gps_alt, 'gps_alt should be none')
