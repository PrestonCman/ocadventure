from django.db import models
from pygments.lexers import get_all_lexers
import lxml.html.clean as html_cleaner, lxml.html as html

LEXERS = [item for item in get_all_lexers() if item[1]]


#Here is the model I created for books.
class Book(models.Model):
    isbn_13 = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
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
    
    def clean_description(self):
        doc = html.fromstring(self.description)
        cleaner = html_cleaner.Cleaner(style=True)
        doc = cleaner.clean_html(doc)
        return doc.text_content()
        
    def __str__(self):
       return self.title
   
class LastONIXFile(models.Model):
    file_path = models.CharField(max_length=250)

    def __str__(self):
        return self.file_path 