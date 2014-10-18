from tastypie.resources import ModelResource
from . import models


class PhotoResource(ModelResource):
    class Meta:
        queryset = models.Photo.objects.all()
        resource_name = 'photo'
