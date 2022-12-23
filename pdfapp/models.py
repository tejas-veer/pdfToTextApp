from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TextModel(models.Model):
    text = models.TextField()
    file_name = models.TextField()
    file_link = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

