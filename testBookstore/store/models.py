from django.db import models
from sanitizer.models import SanitizedCharField
from pygments.lexers import get_all_lexers

LEXERS = [item for item in get_all_lexers() if item[1]]


#Here is the model I created for books.
class Book(models.Model):
    isbn_13 = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    description = SanitizedCharField(max_length=10000, strip=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, null=True, blank = True)
    series = models.CharField(max_length=100,null=True, blank = True)
    volume = models.CharField(max_length=100,null=True, blank = True)
    ready_for_sale = models.BooleanField()
    # should we have multiple places for publisher and author since we might have more than one publisher and author.
    publisher = models.CharField(max_length=100)
    primary_author = models.CharField(max_length=300)
    other_authors = models.CharField(max_length=300,null=True, blank = True)
    class Meta:
        ordering = ['title']
    
    def __str__(self):
       return self.title
   
class LastONIXFile(models.Model):
    file_path = models.CharField(max_length=250)

    def __str__(self):
        return self.file_path 