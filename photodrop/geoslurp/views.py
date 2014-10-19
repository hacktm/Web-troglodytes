from django import shortcuts
from django.contrib import auth
from django.contrib.auth import views as auth_views
from django.template.response import TemplateResponse
from django import http


def index(request):
    return shortcuts.render(request, 'base.html')


def geoslurp_login(request):
    response = auth_views.login(request)
    if request.user.is_authenticated():
        return shortcuts.redirect('geoslurp_home')
    return response


def geoslurp_logout(request):
    auth.logout(request)
    return shortcuts.redirect('geoslurp_home')


