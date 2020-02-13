from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('isbn_13', 'price', 'genre', 'description',
                  'title', 'subtitle', 'series', 'volume',
                  'ready_for_sale', 'publisher', 'primary_author',
                  'other_authors', 'file_path','linenos' )