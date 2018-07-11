from django.db import models


class Post(models.Model):
    body = models.TextField()
    title = models.CharField(max_length=120)

    def get_excerpt(self, char):
        return self.body[:char]
