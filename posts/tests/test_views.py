from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

import pytest
from mixer.backend.django import mixer

from posts.views import HomeView, AdminView, PostUpdateView

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


class TestPostUpdateView:
    def test_get_request(self):
        user = mixer.blend('auth.User')
        req = RequestFactory().get('/')
        req.user = user
        obj = mixer.blend('posts.Post')
        response = PostUpdateView.as_view()(req, pk=obj.pk)
        assert response.status_code == 200, 'Should be callable by registered users'

    def test_post_request(self):
        post = mixer.blend('posts.Post')
        data = {'title': 'Title', 'body': 'Body of the message.'}
        req = RequestFactory().post('/', data=data)
        response = PostUpdateView.as_view()(req, pk=post.pk)
        assert response.status_code == 302, 'Should redirect to success view'
        post.refresh_from_db()
        assert post.title == 'Title', 'Should update title of the post'
        assert post.body == 'Body of the message.', 'Should update body text of the post'
