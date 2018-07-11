import pytest

from posts.forms import PostForm

pytestmark = pytest.mark.django_db


class TestPostForm:
    def test_empty_form(self):
        form = PostForm(data={})
        assert form.is_valid() is False, 'Should be invalid if no data is given'

    def test_form_too_short(self):
        form = PostForm(data={'title': 'Title', 'body': 'Hello'})
        assert form.is_valid() is False, 'Should be invalid if body message is too short'
        assert 'body' in form.errors

    def test_valid_form(self):
        form = PostForm(data={'title': 'Title', 'body': 'Hello world!'})
        assert form.is_valid() is True, 'Should be valid if body message is not too short'