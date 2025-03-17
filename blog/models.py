from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Must be present
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title