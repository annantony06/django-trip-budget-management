from django.urls import path
from .views import (
    augllogin_view,
    signup_view,
    signin_view,
    forgot_view,
    change_password_view,
    dashboard_view,
    trip_packages_view,
    add_companion,
    view_companion,
    delete_companion,
    create_expense,
    view_expenses,
    delete_expense,
    create_budget,
    view_budget,
    update_budget,
    create_offer,
    create_feedback,
    about_us_view,
    PaymentView,
    payment_success,
    success,
    logout_view,
     feedback_success_view, 
   
)

urlpatterns = [
    path('login/', augllogin_view, name='augllogin'),  # Single login view
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('signin/', signin_view, name='signin'),  # Changed name to 'signin'
    path('forgot/', forgot_view, name='forgot_password'),
    path('change_password/', change_password_view, name='change_password'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('trip_packages/', trip_packages_view, name='trip_packages'),
    path('addcompanion/', add_companion, name='add_companion'),
    path('viewcompanion/', view_companion, name='viewcompanion'),  # Example user view
    path('delete/<int:companion_id>/', delete_companion, name='delete_companion'),
    # Expense Management URLs
    path('addexpense/', create_expense, name='create_expense'),
    path('viewexpenses/', view_expenses, name='view_expenses'),
    path('deleteexpense/<int:expense_id>/', delete_expense, name='delete_expense'),
    # Budget Management URLs
    path('addbudget/', create_budget, name='create_budget'),
    path('viewbudget/', view_budget, name='view_budget'),
    path('updatebudget/<int:budget_id>/', update_budget, name='update_budget'),
    # Offers and Feedback URLs
    path('offers/', create_offer, name='create_offer'),
    path('feedback/', create_feedback, name='create_feedback'),
     path('feedbacksucess/', feedback_success_view, name='feedbacksucess'),  # Success page
    # Static Pages
    path('aboutus/', about_us_view, name='about_us_view'),
    # Payment URLs
    path('payment/', PaymentView.as_view(), name='payment'),
    path('paymentsuccess/', payment_success, name='payment_success'),
    path('success/', success, name='success'),  # URL to display success message
    
]