"""
URL configuration for postapp project.

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
from django.urls import path
from django.contrib import admin  # Import the admin module
from django.conf import settings
from django.conf.urls.static import static
from blog import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blogs/create/', views.create_blog, name='blog_create'),
    path('blogs/<int:pk>/edit/', views.edit_blog, name='edit_blog'),
    path('blogs/<int:pk>/delete/', views.delete_blog, name='blog_confirm_delete'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('signup/', views.signup, name='signup'),
    path('admin/', admin.site.urls),  # Add the admin URL
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)