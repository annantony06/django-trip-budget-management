from django.urls import path
from . import views 
from .views import reply_feedback  # Correctly import the views module

app_name = 'staff'  # This is important for namespacing

urlpatterns = [
    path('', views.staff_login_view, name='staff'), 
    path('dashboard/', views.staff_dashboard_view, name='staffdashboard'),  # Staff dashboard view
    path('signin/', views.signin_view, name='staffsignin'),  # Staff signin view
    path('signup/', views.staff_signup_view, name='staff_signup'), 
    path('forgot/', views.staff_forgot_view, name='forgot_password'),  # Correctly reference the forgot password view
    path('change_password/', views.change_password_view, name='change_password'),  # Ensure this view is defined
    path('users/', views.users_view, name='users'),  # Users page
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),  # Delete user
    path('expenses/', views.expenses_view, name='expenses'),  # Expenses page
    path('expenses/delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),  # Delete expense
    path('budget/', views.budget_view, name='budget'),  # Budget page
    path('budget/delete/<int:budget_id>/', views.delete_budget, name='delete_budget'),  # Delete budget
    path('feedback/', views.feedback_view, name='feedback'),  # Feedback page
    path('feedback/reply/<int:feedback_id>/', views.reply_feedback, name='reply_feedback'),  # Reply to feedback
    path('feedback/delete/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
      path('reply/<int:feedback_id>/', reply_feedback, name='reply_feedback'),  # URL for rep  # Delete feedback
      path('feedback/assigned/', views.staff_assigned_feedback_view, name='staffassignedfeedback'),
]