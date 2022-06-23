from django.db import models
from user.models import User
# Create your models here.

class Workspace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="image", null=True)

    def __str__(self) -> str:
        return self.title
