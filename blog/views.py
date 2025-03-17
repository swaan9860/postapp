from django.shortcuts import render, redirect             # Import shortcuts for rendering and redirecting
from django.contrib.auth import authenticate, login, logout  # Import authentication functions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User               # Import Django's User model
from django.contrib import messages                       # Import messages framework for user feedback
from django.shortcuts import render, get_object_or_404    # Import get_object_or_404 for safe object retrieval
from .models import Blog                                  # Import Blog model from current app

def home(request):
    """
    Render the home page.
    """
    return render(request, 'blog/home.html')  # Render home template without context


def blog_list(request):
    """
    Display a list of all blog posts.
    """
    blogs = Blog.objects.all()  # Retrieve all Blog objects from database
    return render(request, 'blog/blog_list.html', {'blogs': blogs})  # Render blog list with blogs in context


def blog_detail(request, pk):
    """
    Display details of a specific blog post.
    Args:
        pk: Primary key of the blog post
    """
    blog = get_object_or_404(Blog, pk=pk)  # Get blog or return 404 if not found
    return render(request, 'blog/blog_detail.html', {'blog': blog})  # Render blog detail with blog in context


# Login View
def user_login(request):
    """
    Handle user login functionality.
    Authenticates users and redirects to dashboard on success.
    """
    if request.method == 'POST':
        # Handle form submission
        username = request.POST['username']  # Extract username from POST data
        password = request.POST['password']  # Extract password from POST data
        user = authenticate(request, username=username, password=password)  # Attempt authentication

        if user is not None:
            # If authentication succeeds
            login(request, user)         # Log the user in, creating a session
            return redirect('home')  # Redirect to blog_list
        else:
            # If authentication fails
            messages.error(request, "Invalid username or password")  # Add error message

    return render(request, 'accounts/login.html')  # Render login template for GET or failed POST

@login_required
def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            Blog.objects.create(title=title, description=description, author=request.user)
            messages.success(request, 'Blog created successfully!')
            return redirect('blog_list')
        else:
            messages.error(request, 'Please fill in all fields.')
    return render(request, 'blog/blog_create.html')

# Logout View
def user_logout(request):
    """
    Handle user logout functionality.
    Logs out the user and redirects to login page.
    """
    logout(request)  # End the user's session
    messages.success(request, "You have been logged out.")  # Add success message
    return redirect('user_login')  # Redirect to login page


# Signup View
def signup(request):
    """
    Handle user registration functionality.
    Creates a new user account and redirects to login on success.
    """
    if request.method == 'POST':
        # Handle form submission
        username = request.POST['username']    # Extract username from POST data
        email = request.POST['email']          # Extract email from POST data
        password1 = request.POST['password1']  # Extract first password entry
        password2 = request.POST['password2']  # Extract password confirmation

        if password1 != password2:
            # Check if passwords match
            messages.error(request, "Passwords do not match")  # Add error message
            return redirect('signup')  # Redirect back to signup page

        if User.objects.filter(username=username).exists():
            # Check if username is already taken
            messages.error(request, "Username already exists")  # Add error message
            return redirect('signup')  # Redirect back to signup page

        # Create new user if validation passes
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()  # Save the new user to database
        messages.success(request, "Account created successfully! Please log in.")  # Add success message
        return redirect('login')  # Redirect to login page

    return render(request, 'accounts/signup.html')  # Render signup template for GET requests


