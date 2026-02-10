from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# User Profile model to extend the default User model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

# Trip Package model to manage different trip packages
class TripPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Set a default user (ID 1 as a placeholder)
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)  # Added location field

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Trip Packages"

    def __str__(self):
        return self.name

class Companion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    trip_package = models.ForeignKey(TripPackage, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Expense model to track user expenses
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip_package = models.ForeignKey(TripPackage, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"{self.amount} - {self.description} on {self.date}"

# Budget model to manage user budgets
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.remaining_budget > self.total_budget:
            raise ValidationError("Remaining budget cannot exceed total budget.")

    def __str__(self):
        return f"{self.user.username} - Budget: {self.total_budget}"

# Offer model to manage travel offers
class Offer(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_until = models.DateField()

    def __str__(self):
        return self.title


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='feedback_images/', null=True, blank=True)
    assigned_to = models.ForeignKey(
        User,  # Or Staff, depending on your staff model
        on_delete=models.SET_NULL,  # Keep feedback if staff is deleted, set assigned_to to null
        null=True,
        blank=True,
        related_name='assigned_feedbacks'  # Allows you to access feedbacks assigned to a staff member
    )
    # Add a status field to track the feedback progress
    STATUS_CHOICES = [
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
    )

    def __str__(self):
        return f"Feedback from {self.user.username} at {self.submitted_at}"
class Payment(models.Model):
    PENDING = 'P'
    COMPLETED = 'C'
    FAILED = 'F'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} - {self.get_status_display()}"