from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include(('myapp.urls', 'myapp'), namespace='myapp')),  # Include user page URLs with namespace
    path('staff/', include(('staff.urls', 'staff'), namespace='staff')),  # Include staff-related URLs with namespace
    path('', RedirectView.as_view(url='/myapp/login/')),  # Redirect root URL to login page
  
]