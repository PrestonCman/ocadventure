from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=200)


    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    num_queries = models.IntegerField()
    
    class Meta:
        ordering = ['last_name']

    def get_name(self):
        return f'{self.last_name}, {self.first_name}'

    def __str__(self):
        output = "{} {}, {}, {}"
        return output.format(self.first_name, self.last_name, self.email, self.company, self.num_queries)
