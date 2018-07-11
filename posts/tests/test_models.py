import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestPost:
    def test_model(self):
        obj = mixer.blend('posts.Post')
        assert obj.pk == 1, 'Should create a post instance'

    def test_get_excerpt(self):
        obj = mixer.blend('posts.Post', body='Hello world!')
        result = obj.get_excerpt(5)
        assert result == 'Hello', 'Should return first 5 characters of a body text field'

