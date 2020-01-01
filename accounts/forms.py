from django.contrib.auth.models import User
from django.forms import ModelForm, Form, CharField, EmailField, PasswordInput, EmailInput, TextInput, DateInput
from accounts.models import Profile

class SignupForm(Form):
    username = CharField(widget=TextInput(attrs={
        'class': 'form-control',
    }))
    password = CharField(widget=PasswordInput(attrs={
        'class': 'form-control',
    }))
    email = EmailField(label='Email', widget=EmailInput(attrs={
        'class': 'form-control',
    }))

    def clean(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            msg = f"Sorry, the username '{username}' is already taken."
            self.add_error('username', msg)

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

        widgets = {
            'birthdate': DateInput(attrs={'type': 'date', 'class': 'form-control w-75',}),
        }