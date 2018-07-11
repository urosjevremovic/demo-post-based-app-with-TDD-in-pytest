from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView

from posts.forms import PostForm
from posts.models import Post


class HomeView(TemplateView):
    template_name = 'posts/home.html'


class AdminView(TemplateView):
    template_name = 'posts/admin.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PostUpdateView(UpdateView):
    template_name = 'posts/update.html'
    model = Post
    form_class = PostForm
    success_url = '/'
