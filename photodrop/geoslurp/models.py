from django.db import models
from django.core import files
from . import transform


class Photo(models.Model):
    # media_id = models.AutoField(primary_key=True)
    description = models.TextField()
    title = models.CharField(max_length=32)
    image = models.ImageField(upload_to='images')

    longitude = models.DecimalField(max_digits=7, decimal_places=3, null=True)
    latitude = models.DecimalField(max_digits=7, decimal_places=3, null=True)
    altitude = models.DecimalField(max_digits=7, decimal_places=3, null=True)

    def save(self, *args, **kwargs):
        location = transform.get_location(self.image)
        self.longitude = location['longitude']
        self.latitude = location['latitude']
        self.altitude = location['altitude']
        super(Photo, self).save(*args, **kwargs)

    def upload_local_image(self, name, path):
        with open(path, 'rb') as file_:
            self.image.save(name, files.File(file_))

    def __unicode__(self):
        return self.title
