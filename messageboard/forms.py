import django.forms as forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

