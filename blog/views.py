from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Blog
from .forms import BlogForm  # Assuming you have a BlogForm for editing blogs

def home(request):
    """
    Render the home page.
    """
    return render(request, 'blog/home.html')

def blog_list(request):
    """
    Display a list of all blog posts.
    """
    blogs = Blog.objects.all()
    return render(request, 'blog/blog_list.html', {'blogs': blogs})

def blog_detail(request, pk):
    """
    Display details of a specific blog post.
    Args:
        pk: Primary key of the blog post
    """
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/blog_detail.html', {'blog': blog})

def user_login(request):
    """
    Handle user login functionality.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')

@login_required
def create_blog(request):
    """
    Handle blog creation with picture upload.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        picture = request.FILES.get('picture')

        if title and description:
            Blog.objects.create(
                title=title,
                description=description,
                author=request.user,
                picture=picture
            )
            messages.success(request, 'Blog created successfully!')
            return redirect('blog_list')
        else:
            messages.error(request, 'Please fill in all required fields (title and description).')
    return render(request, 'blog/blog_create.html')

@login_required
def upload_media(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        picture = request.FILES.get('picture')
        if title and description:
            Blog.objects.create(title=title, description=description, author=request.user, picture=picture)
            messages.success(request, 'Picture uploaded successfully!')
            return redirect('blog_list')
        else:
            messages.error(request, 'Please fill in all required fields.')
    return render(request, 'blog/blog_create.html')

def user_logout(request):
    """
    Handle user logout functionality.
    """
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('user_login')

def signup(request):
    """
    Handle user registration functionality.
    """
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('user_login')

    return render(request, 'accounts/signup.html')

@login_required
def edit_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.user.id != blog.author.id:  # Changed to id for consistency
        messages.error(request, "You do not have permission to edit this blog.")
        return redirect('blog_list')
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog updated successfully!')
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog/blog_edit.html', {'form': form, 'blog': blog})

@login_required
def delete_blog(request, pk):
    """
    Handle deleting a blog post.
    Only the author of the blog can delete it.
    """
    blog = get_object_or_404(Blog, pk=pk)

    # Check if the logged-in user is the author of the blog
    if request.user.id != blog.author.id:
        messages.error(request, "You do not have permission to delete this blog.")
        return redirect('blog_list')

    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog deleted successfully!')
        return redirect('blog_list')

    return render(request, 'blog/blog_confirm_delete.html', {'blog': blog})

from django.conf import settings

def debug_template_paths():
    import os
    print("Django is searching for templates in:")
    for path in settings.TEMPLATES[0]['DIRS']:
        print(f" - {os.path.abspath(path)}")
