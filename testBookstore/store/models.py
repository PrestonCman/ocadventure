from django.db import models

# Create your models here.
# Create your models here.
from django.db import models



#Here is the model I created for books.
class Book(models.Model):
   
    
    isbn_13 = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    description = models.CharField(max_length=700)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, null=True)
    series = models.CharField(max_length=100,null=True)
    volume = models.CharField(max_length=100,null=True)
    ready_for_sale = models.BooleanField()
    # should we have multiple places for publisher and author since we might have more than one publisher and author.
    publisher = models.CharField(max_length=100)
    primary_author = models.CharField(max_length=300)
    other_authors = models.CharField(max_length=100,null=True)
    def __str__(self):
       return self.title
   

    


#Here is the modele for site Book Data
#class Site_book_data():
 #   def __str__(self):
  #      return self
   # book_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    