from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin

from geoslurp.api import PhotoResource
from geoslurp import views

admin.autodiscover()

photo_resource = PhotoResource()

urlpatterns = patterns('',
    url(r'^$', views.index, name='geoslurp_home'),
    url(r'^accounts/login/$',
        views.geoslurp_login, name='accounts_login'),

    url(r'^accounts/logout/$',
        views.geoslurp_logout, name='accounts_logout'),

    # url(r'^accounts/create/$',
    #     views.geoslurp_register, name='accounts_create'),

    # url(r'^accounts/profile/$',
    #     views.ProfileDetailView.as_view(), name='user_profile'),


    url(r'^api/', include(photo_resource.urls)),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
