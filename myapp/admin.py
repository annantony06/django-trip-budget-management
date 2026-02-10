from django.contrib import admin
from .models import UserProfile, TripPackage, Companion, Expense, Budget, Offer, Feedback

class TripPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'location')  # Fields to display in the list view
    search_fields = ('name', 'location')  # Fields to search
    list_filter = ('duration',)  # Add filters for duration

# Custom admin class for Companion
class CompanionInline(admin.TabularInline):
    model = Companion
    extra = 1  # Number of empty forms to display

class TripPackageAdminWithCompanions(TripPackageAdmin):
    inlines = [CompanionInline]  # Allow inline editing of companions in the TripPackage admin

# Custom admin class for Expense
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'date', 'user', 'trip_package')  # Fields to display
    search_fields = ('description',)  # Fields to search
    list_filter = ('date', 'user')  # Add filters for date and user

# Custom admin class for Budget
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_budget', 'remaining_budget', 'created_at')  # Fields to display
    search_fields = ('user__username',)  # Search by username of the user
    list_filter = ('created_at',)  # Filter by creation date

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'submitted_at', 'message')  # Fields to display
    search_fields = ('user__username', 'message')  # Search by username and message
    list_filter = ('submitted_at',) 
# Register your models with the admin site
admin.site.register(UserProfile)
admin.site.register(TripPackage, TripPackageAdminWithCompanions)  # Keep this line
admin.site.register(Companion)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Budget, BudgetAdmin)
admin.site.register(Offer)
admin.site.register(Feedback, FeedbackAdmin)