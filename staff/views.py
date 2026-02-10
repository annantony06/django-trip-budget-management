
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StaffSignupForm, FeedbackForm  # Import your forms
from .models import UserAssignment, Expense, Budget, Feedback  # Import your models
from django.contrib.auth.decorators import user_passes_test
from .models import Staff,Feedback
from django.core.paginator import Paginator 
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import SimplePasswordResetForm 
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Feedback, Staff 
from .forms import FeedbackForm 

def staff_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')  # Get the 'next' URL if it exists
            if next_url:
                return redirect(next_url)  # Redirect to the original page
            return redirect('staff:staffdashboard')  # Default redirect to staff dashboard
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'staff/stafflogin.html')
def staff_signup_view(request):
    """View for staff signup."""
    if request.method == 'POST':
        form = StaffSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('staffsignin')  # Redirect to staffsignin page after signup
    else:
        form = StaffSignupForm()  # Create a new signup form
    return render(request, 'staff/stafflogin.html', {'form': form})  # Render the signup template


def signin_view(request):
    print("Sign-in view called")  # Debug statement

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
             # Redirect to the dashboard or another page
        else:
            messages.error(request, 'Invalid email or password. Please try again.')

    return render(request, 'staff/staffsignin.html') # Render the signin template
def staff_dashboard_view(request):
    return render(request, 'staff/staffdashboard.html')  #ame as needed
def staff_forgot_view(request):
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
                    return render(request, 'staff/staffforgot.html', {'form': form})

            # Set the new password
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password has been reset successfully. You can now log in.')
            return redirect('staff')  # Redirect to login or another page
    else:
        form = SimplePasswordResetForm()

    # Render the forgot password template 
    return render(request, 'staff/staffforgot.html', {'form': form})
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
    return render(request, 'staff/staffchangepassword.html', {'form': form})
@login_required
def users_view(request):
    """View to display the list of users assigned to the staff member."""
    print("Users view called")  # Debug statement

    # Check if the user has a staff profile
    if not hasattr(request.user, 'staff_profile'):
        messages.error(request, 'You do not have a staff profile.')
        return redirect('staff:staffdashboard')  # Redirect to the dashboard if no staff profile

    # Get the staff member
    staff_member = request.user.staff_profile

    # Fetch user assignments for the staff member
    assignments = UserAssignment.objects.filter(staff=staff_member)  # Adjust this line based on your model relationships

    # Debugging: Print the fetched assignments
    print("Fetched assignments:", assignments)

    # Check if there are no assignments
    if not assignments.exists():
        messages.info(request, 'No users assigned to you.')
        return render(request, 'staff/users.html', {'assignments': []})  # Render with an empty list

    # Implement pagination
    paginator = Paginator(assignments, 10)  # Show 10 assignments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare context for rendering
    context = {
        'assignments': page_obj,  # Use 'assignments' to match your template
    }
    
    return render(request, 'staff/users.html', context)
@login_required
def delete_user(request, user_id):
    """View to delete a user."""
    user = get_object_or_404(UserAssignment, id=user_id)  # Get the user object or return a 404 if not found

    if request.method == 'POST':
        user.delete()  # Delete the user
        messages.success(request, 'User  deleted successfully.')  # Show success message
        return redirect('users')  # Redirect to the users view

    # If the request method is GET, render the confirmation template
    return render(request, 'staff/dltuser.html', {'user': user})  # Render the delete confirmation template
@login_required
def expenses_view(request):
    """View to display the expenses for the staff member."""
    if not hasattr(request.user, 'staff_profile'):
        messages.error(request, 'You do not have a staff profile.')
        return redirect('staff:staffdashboard')  

    # Fetch expenses from the admin interface
    try:
        expenses = Expense.objects.all()  # Fetch all expenses
    except Exception as e:
        messages.error(request, f'Error fetching expenses: {str(e)}')
        expenses = []

    context = {'expenses': expenses}
    return render(request, 'staff/expenses.html', context)
@login_required
def delete_expense(request, expense_id):
    """View to delete an expense."""
    expense = get_object_or_404(Expense, id=expense_id)  # Get the expense object or return a 404 if not found

    # Check if the logged-in user is the owner of the expense
    if expense.user != request.user:
        messages.error(request, 'You do not have permission to delete this expense.')
        return redirect('expenses')  # Redirect to the expenses view

    if request.method == 'POST':
        expense.delete()  # Delete the expense
        messages.success(request, 'Expense deleted successfully.')  # Show success message
        return redirect('expenses')  # Redirect to the expenses view

    # If the request method is GET, render the confirmation template
    return render(request, 'staff/dltexpense.html', {'expense': expense})  # Render the delete confirmation template

@login_required
def budget_view(request):
    """View to display the budgets for the staff member."""
    try:
        # Fetch the budgets associated with the logged-in user
        budgets = Budget.objects.filter(user=request.user)

        # Initialize total_budget and remaining_budget
        total_budget = 0
        remaining_budget = 0

        # Calculate total budget and remaining budget
        for budget in budgets:
            total_budget += budget.total_amount
            remaining_budget += budget.remaining_amount

        # Handle case where no budgets exist
        if not budgets.exists():
            messages.info(request, 'No budgets found for this user.')
            total_budget = None
            remaining_budget = None

        # Fetch the user's email from the user object
        user_email = request.user.email

    except Exception as e:
        messages.error(request, f'Error fetching budgets: {str(e)}')
        total_budget = None  # Set to None if there's an error
        remaining_budget = None  # Set to None if there's an error
        user_email = request.user.email  # Use the user's email

    # Render the view budget template with the budgets
    context = {
        'total_budget': total_budget,
        'remaining_budget': remaining_budget,
        'total_budget_user': user_email,
        'budgets': budgets,  # Ensure this is included
    }
    return render(request, 'staff/budget.html', context)

@login_required
def delete_budget(request, budget_id):
    """View to delete a budget."""
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)  # Ensure the budget belongs to the user

    if request.method == 'POST':
        budget.delete()  # Delete the budget
        messages.success(request, 'Budget deleted successfully.')  # Show success message
        return redirect('budget_view')  # Redirect to the budget view

    # If the request method is GET, render the confirmation template
    return render(request, 'staff/dltbudget.html', {'budget': budget})  # Render the delete confirmation template
@login_required
def feedback_view(request):
    """View for staff to see all feedback."""
    if not request.user.is_staff:
        # Redirect to another page or show an error message
        return redirect('staff:staffsignin')  # Example: redirect to staff login

    feedbacks = Feedback.objects.all().order_by('-created_at')
    context = {'feedbacks': feedbacks}
    return render(request, 'staff/feedback.html', context)
@login_required
def reply_feedback(request, feedback_id):
    """View for staff to reply to feedback."""
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.method == 'POST':
        reply_message = request.POST.get('reply')
        feedback.reply = reply_message  # Use the reply field in the Feedback model
        feedback.save()
        messages.success(request, 'Reply sent successfully.')
    return render(request, 'staff/replyfeedback.html', {'feedback': feedback})  # Render the reply feedback template
@login_required
def delete_feedback(request, feedback_id):
    """View to delete feedback."""
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'Feedback deleted successfully.')
        return redirect('feedback')  # Redirect to the feedback view
    return render(request, 'staff/dltfeedback.html', {'feedback': feedback})  # Render the delete confirmation template
@login_required
@user_passes_test(lambda u: u.is_superuser)  # Only allow superusers to access
def staff_view(request):
    """View to display all staff members."""
    staff_members = Staff.objects.all()  # Get all staff members
    return render(request, 'staff/staff_list.html', {'staff_members': staff_members})
def reply_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    # Logic to handle the reply goes here
    return render(request, 'staff/replyfeedback.html', {'feedback': feedback})
@login_required
def staff_assigned_feedback_view(request):
    # Get the currently logged-in user's staff instance
    staff_user = Staff.objects.get(user_id=request.user.id)  # Fetch the staff instance related to the logged-in user

    # Fetch feedback assigned to this staff member
    assigned_feedback = Feedback.objects.filter(staff=staff_user).order_by('-created_at')

    context = {
        'assigned_feedback': assigned_feedback
    }

    return render(request, 'staff/staffassignedfeedback.html', context)