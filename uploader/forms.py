from django import forms
from django.core.exceptions import ValidationError

from uploader.models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class FileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)


    class Meta:
        model = File
        fields = ('description', 'file',)


class MemberCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(MemberCreationForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].label or 'Email Address'
        self.fields['password1'].widget.attrs['placeholder'] = self.fields['password1'].label or 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = self.fields['password2'].label or 'Re-password'

    class Meta(UserCreationForm.Meta):
        model = Member
        fields = ('email', 'password1', 'password2')


class MemberChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(MemberChangeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Member
        fields = ('email',)


class MemberLoginForm(forms.Form):
    email = forms.EmailField(label="Email address", required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    password = forms.CharField(label="Password", required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class EditProfileForm(forms.Form):
    email = forms.EmailField(label="Email address", required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="First name", required=False,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(label="Last name", required=False,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    avatar = forms.FileField(required=False)

