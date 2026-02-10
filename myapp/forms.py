# myapp/forms.py

from django import forms
from .models import UserProfile, TripPackage, Companion, Expense, Budget, Offer, Feedback

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'birth_date']  # Fields for user profile

class TripPackageForm(forms.ModelForm):
    class Meta:
        model = TripPackage
        fields = ['name', 'description', 'price', 'duration', 'location']  # Fields for trip package

class CompanionForm(forms.ModelForm):
    class Meta:
        model = Companion
        fields = ['user', 'trip_package', 'relationship']  # Fields for companion

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['trip_package', 'amount', 'description', 'date']  # Fields for expense

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['total_budget', 'remaining_budget']  # Fields for budget

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['title', 'description', 'discount_percentage', 'valid_until']  # Fields for offer

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message', 'image']  # Include the image field for feedback
class SimplePasswordResetForm(forms.Form):
    username_or_email = forms.CharField(label="Username or Email", max_length=254)
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")