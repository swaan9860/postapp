from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    # Form based on the Blog model
    class Meta:
        # Specify the model to base the form on
        model = Blog
        # Fields to include in the form; 'author' and 'created_at' are excluded as they’re handled automatically
        fields = ['title', 'description', 'picture']