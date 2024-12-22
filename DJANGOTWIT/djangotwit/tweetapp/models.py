from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

#Model adı oluşturuldu.
class Tweet(models.Model):
    username= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message= models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)  # Gönderi zamanı


    def __str__(self):
        return f"Tweet nick: {self.username} message: {self.message}"