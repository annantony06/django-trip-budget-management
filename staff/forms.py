from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Feedback

class StaffSignupForm(UserCreationForm):
    """Form for staff signup."""
    email = forms.EmailField(required=True)  # Add an email field

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Fields to include in the form

    def save(self, commit=True):
        user = super().save(commit=False)
        # You can add additional logic here if needed
        if commit:
            user.save()
        return user

class FeedbackForm(forms.ModelForm):
    """Form for submitting feedback."""
    class Meta:
        model = Feedback
        fields = ('message',)  # Fields to include in the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({'placeholder': 'Enter your feedback here...', 'rows': 4})

class SimplePasswordResetForm(forms.Form):
    """Form for resetting password."""
    username_or_email = forms.CharField(label="Username or Email", max_length=254)
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput)