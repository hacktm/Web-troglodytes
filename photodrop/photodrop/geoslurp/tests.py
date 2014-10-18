import os

from django.test import TestCase
from django.core import files

from . import models


class TestPhoto(TestCase):
    def test_upload(self):
        title = 'kittey.jpg'
        photo = models.Photo.objects.create(title=title)
        photo.upload_local_image(title, '/home/stz/Pictures/kittey.jpg')

    
