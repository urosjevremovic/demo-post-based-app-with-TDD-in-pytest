from django.contrib.admin.sites import AdminSite

import pytest
from mixer.backend.django import mixer

from posts import models, admin

pytestmark = pytest.mark.django_db


class TestPostAdmin:

    def test_excerpt(self):
        site = AdminSite()
        post_admin = admin.PostAdmin(models.Post, site)

        obj = mixer.blend('posts.Post', body='Hello world!')
        result = post_admin.excerpt(obj)
        assert result == 'Hello', 'Should return first 5 characters of a body text field'
