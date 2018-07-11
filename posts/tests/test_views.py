from django.contrib.auth.models import AnonymousUser
from django.core import mail
from django.http import Http404
from django.test import RequestFactory

import pytest
from mixer.backend.django import mixer
from mock import patch

from posts.views import HomeView, AdminView, PostUpdateView, PaymentView

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
        user = mixer.blend('auth.User')
        post = mixer.blend('posts.Post')
        data = {'title': 'Title', 'body': 'Body of the message.'}
        req = RequestFactory().post('/', data=data)
        req.user = user
        response = PostUpdateView.as_view()(req, pk=post.pk)
        assert response.status_code == 302, 'Should redirect to success view'
        post.refresh_from_db()
        assert post.title == 'Title', 'Should update title of the post'
        assert post.body == 'Body of the message.', 'Should update body text of the post'

    def test_security(self):
        user = mixer.blend('auth.User', first_name='Crash')
        post = mixer.blend('posts.Post')
        req = RequestFactory().post('/', data={'title': 'Title', 'body': 'This will fail to submit'})
        req.user = user
        with pytest.raises(Http404):
            PostUpdateView.as_view()(req, pk=post.pk)


class TestPaymentView:
    @patch('posts.views.stripe')
    def test_payment(self, mock_stripe):
        mock_stripe.Charge.return_value = {'id': '1234'}
        req = RequestFactory().post('/', data={'token': '123'})
        response = PaymentView.as_view()(req)
        assert response.status_code == 302, 'Should redirect to success url'
        assert len(mail.outbox) == 1, 'Should send an email'
