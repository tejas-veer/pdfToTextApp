from django.db import models

# Create your models here.
class TextModel(models.Model):
    text = models.TextField()
    file_name = models.TextField()
    file_link = models.TextField()

