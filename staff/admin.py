from django.contrib import admin
from .models import UserAssignment, Expense, Budget, Feedback, Staff  # Import your models

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'department')  # Fields to display in the list view
    search_fields = ('user__username', 'position')  # Enable search by username and position

@admin.register(UserAssignment)
class UserAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff')  # Fields to display in the list view
    search_fields = ('user__username',)  # Enable search by username

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'description', 'date')  # Fields to display
    list_filter = ('date',)  # Enable filtering by date
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'remaining_amount', 'created_at')  # Ensure these fields exist
    list_filter = ('created_at',)  # Ensure this field exists

admin.site.register(Budget, BudgetAdmin)
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff', 'message', 'created_at')
    search_fields = ('user__username', 'message')
    list_editable = ('staff',)  # Make the 'staff' field editable in the list view

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'staff':
            kwargs['queryset'] = Staff.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)