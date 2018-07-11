from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

import pytest
from mixer.backend.django import mixer

from posts.views import HomeView, AdminView

pytestmark = pytest.mark.django_db


class TestHomeView:
    def test_anonymous_user(self):
        req = RequestFactory().get('/')
        response = HomeView.as_view()(req)
        assert response.status_code == 200, 'Should be callable by anyone'


class TestAdminView:
    def test_anonymous_user(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        response = AdminView.as_view()(req)
        assert 'login' in response.url, 'Anonymous user can\'t see all posts'

    def test_super_user(self):
        user = mixer.blend('auth.User', is_superuser=True)
        req = RequestFactory().get('/')
        req.user = user
        response = AdminView.as_view()(req)
        assert response.status_code == 200, 'Super user can access all posts'
