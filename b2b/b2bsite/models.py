from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Bookstore(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=100)
    company_email = models.CharField(max_length=60)
    bookstores = models.ManyToManyField(Bookstore)

    class Meta:
        ordering = ['name']
        permissions = (
            ('group_user', 'Can Only View Their Company'),
            ('group_admin', 'Can View All Companies')
        )

    def display_bookstores(self):
        return ', '.join(bookstore.name for bookstore in self.bookstores.all())

    display_bookstores.short_description = 'Bookstore'

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    num_queries = models.IntegerField(default=0)

    def __str__(self):
        output = "{} {}, {}, {}"
        return output.format(self.name, self.email, self.company, self.num_queries)
