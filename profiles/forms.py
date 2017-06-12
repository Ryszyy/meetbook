from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class Form_register(forms.Form):
    # name = forms.CharField(label="Name", max_length=40)
    # last_name = forms.CharField(label="Last Name", max_length=40)
    login = forms.CharField(label="Login")
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_bis = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(Form_register, self).clean()
        password = self.cleaned_data.get('password')
        password_bis = self.cleaned_data.get('password_bis')
        email = self.cleaned_data.get('email')
        login = self.cleaned_data.get('login')
        try:
            login = login.lower()
        except:
            pass
        if password != password_bis:
            raise forms.ValidationError("Passwords are not identical.")

        # obj = User.objects.get()
        if User.objects.filter(username=login).exists():
            raise forms.ValidationError("Login already exists")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already taken")
        return self.cleaned_data


class Form_login(forms.Form):
    username = forms.CharField(label="")
    password = forms.CharField(label="", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(Form_login, self).clean()
        username = self.cleaned_data.get('username').lower()
        password = self.cleaned_data.get('password')
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Wrong login or password")
        return self.cleaned_data


class Form_update_user(forms.Form):
    first_name = forms.CharField(label="Forename")
    last_name = forms.CharField(label="Surname")
    bio = forms.CharField(label='Bio', widget=forms.Textarea)
    location = forms.CharField(label="City")
    picture = forms.ImageField(label="Picture")


class Form_update_user_later(forms.Form):
    bio = forms.CharField(label='Bio', widget=forms.Textarea)
    location = forms.CharField(label="City")
    picture = forms.ImageField(label="Picture")
