from django.contrib.auth.models import User
from django.db import models
 
class Office(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    adress = models.CharField(max_length=300)