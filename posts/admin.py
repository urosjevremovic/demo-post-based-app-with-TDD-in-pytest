from django.contrib import admin

from posts.models import Post


class PostAdmin(admin.ModelAdmin):

    model = Post
    list_display = ('title', 'excerpt', )

    def excerpt(self, obj):
        return obj.get_excerpt(5)

admin.site.register(Post, PostAdmin)

