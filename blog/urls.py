from django.urls import path
from . import views
from django.conf import settings  # Import settings to access DEBUG, MEDIA_URL, etc.
from django.conf.urls.static import static  # Import static to serve media files

from django.urls import path
from django.contrib import admin  # Import the admin module
from blog import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('create/', views.create_blog, name='blog_create'),
    path('blogs/<int:pk>/edit/', views.edit_blog, name='blog_edit'),  # Added
    path('signup/', views.signup, name='signup'),  # Added
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)