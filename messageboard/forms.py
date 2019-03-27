import django.forms as forms

from messageboard.models import Post, Board


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_username(self):
        return self.cleaned_data['username'].strip()


class NewPostForm(forms.ModelForm):
    title = forms.CharField(min_length=3)

    class Meta:
        model = Post
        fields = ["title", "body"]

class NewBoardForm(forms.ModelForm):
    name = forms.CharField(required=True)
    class Meta:
        model=Board
        fields = ["name", "description"]