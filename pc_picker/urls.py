"""
URL configuration for pc_picker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.urls import include
from django.views.generic import RedirectView
#from . import views
handler404 = 'parts.views.error'  # Handles 404 errors
handler500 = 'parts.views.error'

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('accounts/', include('django.contrib.auth.urls')), 
    path('about-us/', include('parts.urls')),  # Ensure correct URL pattern
    path('contacts/', include('parts.urls')),
    path('typography/', include('parts.urls')),
    path('', include('parts.urls')),  # This should only be included once
    
]




