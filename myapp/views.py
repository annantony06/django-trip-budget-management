from django.shortcuts import render, redirect, get_object_or_404  # Ensure this import is present
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Companion
from .models import Expense   
from .models import Budget 
from django.contrib.auth.tokens import default_token_generator 
from .forms import CompanionForm, TripPackageForm, ExpenseForm, BudgetForm, OfferForm, FeedbackForm
from django.contrib.auth.forms import PasswordResetForm 
from .models import Payment
from django.views import View 
from django.contrib.auth.models import User
from django import forms
from .models import TripPackage 
from .models import Expense, Budget, Offer
from django.contrib.auth.forms import PasswordChangeForm 
from django.contrib.auth import update_session_auth_hash 
from django.contrib.auth.views import LoginView
from .forms import SimplePasswordResetForm
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Feedback 
from django.utils import timezone
from .models import UserProfile 
from django.middleware.csrf import get_token  
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('auglogin')  #
@login_required
def change_password_view(request):
    print(f"User  is authenticated: {request.user.is_authenticated}")  # Debugging line
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change_done')  # Redirect to a success page
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/changepassword.html', {'form': form})

def augllogin_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('myapp:dashboard')  # Redirect to the dashboard
        else:
            context = {
                'error': 'Invalid credentials',
                'csrf_token': get_token(request)
            }
            return render(request, 'myapp/auglogin.html', context)

    # For GET request, pass CSRF token manually for debug
    context = {
        'csrf_token': get_token(request)
    }
    return render(request, 'myapp/auglogin.html', context)
def signup_view(request):
    """Handle user signup and create UserProfile directly."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the email is already in use
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return render(request, 'myapp/auglogin.html', {'signup_form': True})

        if password == confirm_password:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name
            user.save()

            # ✅ Directly create the UserProfile
            UserProfile.objects.create(user=user)

            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('myapp:augllogin')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'myapp/auglogin.html', {'signup_form': True})#that the signup form should be shown
def signin_view(request):
    """Render the welcome user page."""
    return render(request, 'myapp/augsigin.html')  # Render the welcome user page


    
def forgot_view(request):
    """View to handle forgot password functionality."""
    if request.method == 'POST':
        form = SimplePasswordResetForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            new_password = form.cleaned_data['new_password']

            # Try to find the user by username or email
            try:
                user = User.objects.get(username=username_or_email)  # Check by username
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=username_or_email)  # Check by email
                except User.DoesNotExist:
                    messages.error(request, "No user found with that username or email.")
                    return render(request, 'myapp/forgot.html', {'form': form})

            # Set the new password
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password has been reset successfully. You can now log in.')
            return redirect('augllogin')  # Redirect to login or another page
    else:
        form = SimplePasswordResetForm()

    # Render the forgot password template 
    return render(request, 'myapp/forgot.html', {'form': form})

def reset_view(request):
    """Render the reset password page and handle password reset requests."""
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                use_https=request.is_secure(),
                token_generator=default_token_generator,
                from_email='your_email@gmail.com',  # Replace with your email
                email_template_name='myapp/password_reset_email.html',
                subject_template_name='myapp/password_reset_subject.txt',
                request=request,  # Keep this line
            )
            messages.success(request, 'Password reset email has been sent.')
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()

    return render(request, 'myapp/reset.html', {'form': form})
def dashboard_view(request):
    """Render the welcome user page."""
    return render(request, 'myapp/dashboard.html')  # Render the welcome user page
@login_required
def add_companion(request):
    if request.method == 'POST':
        relationship = request.POST.get('relationship')
        name = request.POST.get('name')
        age = request.POST.get('age')
        trip_package_id = request.POST.get('trip_package')  # Get the selected trip package ID
        
        # Create a new Companion instance
        companion = Companion(
            user=request.user,  # Assuming the user is logged in
            relationship=relationship,
            name=name,
            age=age,
            trip_package_id=trip_package_id  # Set the trip package
        )
        companion.save()  # Save the companion to the database
        
        return redirect('viewcompanion')  # Redirect to the view companions page

    # If GET request, retrieve trip packages to display in the form
    trip_packages = TripPackage.objects.all()  # Get all trip packages
    return render(request, 'myapp/addcompanion.html', {'trip_packages': trip_packages})  # Render the form with trip packages the form with trip packages
@login_required
def view_companion(request):
    """View to display all companions for the logged-in user."""
    print("View Companion called")  # Debug statement

    # Fetch companions for the logged-in user
    companions = Companion.objects.filter(user=request.user)

    # Prepare context for rendering
    context = {
        'companions': companions,
    }

    return render(request, 'myapp/viewcompanion.html', context)

@login_required
def delete_companion(request, companion_id):
    companion = Companion.objects.get(id=companion_id)
    companion.delete()
    return redirect('viewcompanion')  # Rthe companions list


def trip_packages_view(request):
    packages = TripPackage.objects.all()  # Retrieve all TripPackage objects
    context = {
        'packages': packages  # Pass the packages to the template
    }
    return render(request, 'myapp/trip.html', context)  # Ensure the path is correct
    
    # Render the template with the context
     # Use 'trip.html' as the template name
@login_required
def create_expense(request):
    """View to create a new Expense."""
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Set the user to the currently logged-in user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('dashboard')  # Redirect to the dashboard or another page
    else:
        form = ExpenseForm()
    return render(request, 'myapp/addexpense.html', {'form': form})

@login_required
def view_expenses(request):
    """View to display all expenses for the logged-in user."""
    expenses = Expense.objects.filter(user=request.user).select_related('trip_package')

    context = {
        'expenses': expenses,
    }

    return render(request, 'myapp/viewexpense.html', context)
@login_required
def delete_expense(request, expense_id):
    """View to delete an expense."""
    expense = get_object_or_404(Expense, id=expense_id)

    if request.method == 'POST':
        expense.delete()  # Delete the expense
        messages.success(request, 'Expense deleted successfully!')
        return redirect('view_expenses')  # Redirect to the view expenses page

    return render(request, 'myapp/dltexpense.html', {'expense': expense})  # Render the delete confirmation templateelete confirmation template


@login_required
def create_budget(request):
    """View to create a new Budget."""
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)  # Create a budget instance but don't save to the database yet
            budget.user = request.user  # Set the user to the currently logged-in user
            budget.remaining_budget = budget.total_budget  # Initialize remaining budget
            budget.save()  # Save the budget instance to the database
            messages.success(request, 'Budget created successfully!')
            return redirect('view_budget')  # Redirect to the view budget page
    else:
        form = BudgetForm()  # Create a new form instance for GET requests

    return render(request, 'myapp/addbudget.html', {'form': form})  # Renwelcome user Render the template with the form
@login_required
def view_budget(request):
    """View to display the user's budget."""
    print("View Budget called")  # Debug statement

    # Get the user's budget
    budget = Budget.objects.filter(user=request.user).first()  # Fetch the first budget for the user

    # Prepare context for rendering
    context = {
        'budget': budget,
    }

    return render(request, 'myapp/viewbudget.html', context)#r the view budget templateet templateet template
@login_required
def update_budget(request, budget_id):
    """View to update an existing budget."""
    budget = get_object_or_404(Budget, id=budget_id)  # Get the budget object or return a 404 if not found

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)  # Bind the form to the existing budget instance
        if form.is_valid():
            form.save()  # Save the updated budget
            messages.success(request, 'Budget updated successfully!')
            return redirect('view_budget')  # Redirect to the view budget page
    else:
        form = BudgetForm(instance=budget)  # Create a form instance with the existing budget data

    return render(request, 'myapp/updatebudget.html', {'form': form, 'budget': budget})  # Render tender the update form
# Offer View
@login_required
def create_offer(request):
    """View to display all offers."""
    offers = Offer.objects.all()  # Fetch all offers from the database
    return render(request, 'myapp/offers.html', {'offers': offers})  #

@login_required
def create_feedback(request):
    """View to create new Feedback."""
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('myapp:feedbacksucess')
    else:
        form = FeedbackForm()

    # --- Code to set a default feedback ---
    default_feedback_message = "very good"
    default_user = request.user  # Use the currently logged-in user
    Feedback.objects.create(user=default_user, message=default_feedback_message, submitted_at=timezone.now())
    print(f"Default feedback submitted by user: {default_user.username}") # Optional logging

    return render(request, 'myapp/feedback.html', {'form': form})

@login_required
def feedback_success_view(request):
    """View to display a success message after feedback submission."""
    return render(request, 'myapp/feedbacksucess.html')  # R
def about_us_view(request):
    """Render the About Us page."""
    return render(request, 'myapp/aboutus.html')  # Render the About Us page


class PaymentView(View):
    def get(self, request):
        return render(request, 'myapp/payment.html')

    def post(self, request):
        amount = request.POST.get('amount')
        # Simulate payment processing
        payment = Payment.objects.create(amount=amount, status=Payment.PENDING)
        payment.status = Payment.COMPLETED  # or Payment.FAILED based on the response
        payment.save()

        return redirect('myapp:payment_success')  # Redirect to the payment success page

def payment_success(request):
    """View to display the payment success message."""
    return render(request, 'myapp/paymentsuccess.html')  # Ensure this path is correct

def success(request):
    """View to display the success message."""
    return render(request, 'myapp/success.html')  # Ensure the path is correct

    
    