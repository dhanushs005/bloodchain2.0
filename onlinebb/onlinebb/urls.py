"""
URL configuration for onlinebb project.

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
from django.urls import path
from Main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('emergency',views.emerg,name='emergency'),
    path('update',views.save_user_details,name='update'),
    path('donors',views.view_donors,name='donors'),
    path('report', views.report, name='report'),
    path('update-report',views.updateReport,name='updateReport'),
    path('update-emergency',views.emergency_details,name='updateEmergency'),
]
