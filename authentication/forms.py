# authentication/forms.py
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name', 'id':'firstNameField', 'autofocus': True}),
        required=True
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name', 'id':'lastField'}),
        required=True
    )
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username', 'id':'usernameField'}),
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email', 'id': 'emailField'}),
        required=True
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password', 'id': 'passwordField'}),
        required=True,
        strip=False,
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        required=True,
        strip=False,
    )
    
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].error_messages = {
            'password_too_short': "This password is too short. It must contain at least 8 characters. ",
            'password_common': "This password is too common. ",
            'password_numeric': "This password is entirely numeric."
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')

        # Custom validation logic
        if email and get_user_model().objects.filter(email=email).exists():
            self.add_error('email', 'This email is already in use.')
        if username and get_user_model().objects.filter(username=username).exists():
            self.add_error('username', 'This username is already taken.')

        password2_errors = self.errors.get('password2')
        if password2_errors:
            combined_message = ' '.join(password2_errors)
            self.add_error('password2', combined_message)
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        required=True
    )
    password = forms.CharField(
        label="Password",
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        required=True
    )
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'

