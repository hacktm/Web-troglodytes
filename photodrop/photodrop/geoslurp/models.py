from django.db import models
from django.core import files


class Photo(models.Model):
    media_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    # url = models.URLField(max_length=100)
    image = models.ImageField(upload_to='images')
    description = models.TextField()
    longitude = models.DecimalField(max_digits=7, decimal_places=3, null=True)
    latitude = models.DecimalField(max_digits=7, decimal_places=3, null=True)
    altitude = models.DecimalField(max_digits=7, decimal_places=3, null=True)

    def upload_local_image(self, name, path):
        with open(path, 'rb') as file_:
            self.image.save(name, files.File(file_))


    def __unicode__(self):
        return self.title
