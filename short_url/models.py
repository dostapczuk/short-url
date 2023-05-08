from django.db import models

# Create your models here.


class ShortUrl(models.Model):
    alias = models.CharField(unique=True, primary_key=True, max_length=6)
    url = models.CharField(max_length=200)
