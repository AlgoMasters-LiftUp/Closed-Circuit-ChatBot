from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth import password_validation


def validate_email(value):
    if User.objects.filter(email = value).exists():
        raise ValidationError((f"{value} is taken."),params = {'value':value})

username_validator = UnicodeUsernameValidator()

class SignupForm(UserCreationForm):
    def clean_first_name(self):
        if self.cleaned_data["first_name"].strip() == '':
            raise ValidationError("First name is required.")
        return self.cleaned_data["first_name"]
    def clean_last_name(self):
        if self.cleaned_data["last_name"].strip() == '':
            raise ValidationError("Last name is required.")
        return self.cleaned_data["last_name"]
    # def clean_username(self):
    #     if self.cleaned_data["username"].strip() == '':
    #         raise ValidationError("Username is required.")
    #     return self.cleaned_data["username"]
    def clean_email(self):
        if self.cleaned_data["email"].strip() == '':
            raise ValidationError("E-mail is required.")
        return self.cleaned_data["email"]

    first_name = forms.CharField(
                                max_length=25, 
                                min_length=4, 
                                required=True, 
                                help_text='Required: First Name',
                                widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter first name'}))
    
    last_name = forms.CharField(
                            max_length=25, 
                            min_length=2, 
                            required=True, 
                            help_text='Required: Last Name',
                            widget=(forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter last name'})))

    email = forms.EmailField(
                            max_length=200, 
                            required=True, 
                            help_text='Required: Email', 
                            validators = [validate_email],
                            widget=(forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Enter your email address'})))
    
    password1 = forms.CharField(
        # label=('Password'),
        widget=(forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Enter password'})),
        help_text=password_validation.password_validators_help_text_html())
    
    password2 = forms.CharField(
        # label=('Password'),
        widget=(forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Validate password'})),
        help_text=password_validation.password_validators_help_text_html())

    # username = forms.CharField(
    #     # label=('Username'),
    #     max_length=50,
    #     min_length=5, 
    #     required=True,
    #     help_text=('Required. 50 characters or fewer, more than 5 characters. Letters, digits and @/./+/-/_ only.'),
    #     validators=[username_validator],
    #     error_messages={'unique': ("A user with that username already exists.")},
    #     widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter username'})
    # )

    

    class Meta:
        model = User 
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user 