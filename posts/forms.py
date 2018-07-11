from django import forms

from posts.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')

    def clean_body(self):
        data = self.cleaned_data.get('body')
        if len(data) <= 5:
            raise forms.ValidationError('Message is too short')
        return data