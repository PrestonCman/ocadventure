from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200) 
    company = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    num_queries = models.IntegerField()
    
    def __str__(self):
        return self.name