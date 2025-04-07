# models.py
from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    # Title of the blog post, limited to 200 characters
    title = models.CharField(max_length=200)
    
    # Detailed description of the blog post, no length limit
    description = models.TextField()
    
    # ForeignKey linking to the User model; if the user is deleted, the blog is deleted too
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Automatically set to the current timestamp when the blog is created; allows null for flexibility
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    # Field to store an image; uploaded to 'blog_pictures/' folder; optional (null=True, blank=True)
    picture = models.ImageField(upload_to='blog_pictures/', null=True, blank=True)

    # String representation of the model, returns the blog title
    def __str__(self):
        return self.title