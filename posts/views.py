import stripe
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView, View

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

    def post(self, request, *args, **kwargs):
        if getattr(request.user, 'first_name', None) == 'Crash':
            raise Http404()
        return super().post(request, *args, **kwargs)


class PaymentView(View):
    def post(self, request, *args, **kwargs):
        charge = stripe.Charge.create(
            amount=100,
            currency='usd',
            description='',
            token=request.POST.get('token'),
        )
        send_mail(
            'Payment received',
            'Charge {} succeeded'.format(charge['id']),
            'test_me@test.com',
            ['admin@test.com', ],
        )
        return redirect('/')