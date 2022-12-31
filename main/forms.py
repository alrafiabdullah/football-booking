from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox, ReCaptchaV3


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=30, min_length=4, required=True, help_text='30 characters or fewer. Letters, digits and @/./+/-/_ only.',
        error_messages={'unique': 'A user with that username already exists.'},
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autofocus': True})
    )

    email = forms.EmailField(
        max_length=254, required=True, help_text='Enter a valid email address for verification.',
        error_messages={'unique': 'A user with that email already exists.'},
        widget=forms.EmailInput(attrs={'class': 'form-control register-item'}),
    )

    password1 = forms.CharField(
        max_length=30, min_length=8, required=True,
        empty_value='password', label="Password", help_text='Your password can\'t be too similar to your other personal information. Your password must contain at least 8 characters. Your password can\'t be a commonly used password. Your password can\'t be entirely numeric.',
        widget=forms.PasswordInput(attrs={'class': 'form-control register-item',
                                          'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        max_length=30, min_length=8, required=True, help_text='Enter the same password as before.',
        empty_value='password', label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'autocomplete': 'new-password'})
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV3(
            attrs={
                'data-theme': 'dark',
            }
        ), label="This form is protected by Google reCAPTCHA.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'A user with that email already exists.')
        return email

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.is_active = False
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomUserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=30, min_length=4, required=True, help_text='Enter your username.',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autofocus': True})
    )

    password = forms.CharField(
        max_length=30, min_length=4, required=True,
        empty_value='password', label="Password", help_text='Enter your password.',
        widget=forms.PasswordInput(attrs={'class': 'form-control register-item',
                                          'autocomplete': 'new-password'}),
    )

    def clean(self):
        cleaned_data = super(CustomUserLoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = User.objects.filter(username=username).first()
            if user is not None and not user.is_active:
                raise forms.ValidationError(
                    'The account is not active. Please check your email and verify!')
            if user:
                if not user.check_password(password):
                    raise forms.ValidationError('Invalid password')
            else:
                raise forms.ValidationError('Invalid username')

        return cleaned_data
