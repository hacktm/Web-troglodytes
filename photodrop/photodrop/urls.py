from django.conf.urls import patterns, include, url

from django.contrib import admin

from geoslurp.api import PhotoResource

admin.autodiscover()

photo_resource = PhotoResource()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'photodrop.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^api/', include(photo_resource.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
