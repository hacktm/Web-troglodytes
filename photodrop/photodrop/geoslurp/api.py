from tastypie.resources import ModelResource
from tastypie import authorization
from . import models


class PhotoResource(ModelResource):

    def deserialize(self, request, data, format='application/json'):
        """Sweet baby jesus, do not remove this method!!!"""
        if format is None:
            format = request.META.get('CONTENT_TYPE', 'application/json')

        if format == 'application/x-www-form-urlencoded':
            deserialized = request.POST
        elif format.startswith('multipart'):
            deserialized = request.POST.copy()
            deserialized.update(request.FILES)
        else:
           deserialized = self._meta.serializer.deserialize(request.raw_post_data, format=format)
        return deserialized


    class Meta:
        queryset = models.Photo.objects.all()
        resource_name = 'photo'
        authorization = authorization.Authorization()
