from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField


#Here is the model I created for books.
class Book():
    def __str__(self):
        return self
    
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
    publisher = ArrayField(models.CharField(max_length=100))
    author = ArrayField(models.CharField(max_length=300))


   

    


#Here is the modele for site Book Data
#class Site_book_data():
 #   def __str__(self):
  #      return self
   # book_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    