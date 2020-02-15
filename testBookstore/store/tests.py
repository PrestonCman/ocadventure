from django.test import TestCase
import requests
# Create your tests here.

filepath = "/idiot.txt"

book = {
    'isbn_13':'This is the', 
    'price':'test', 
    'genre':'test',
    'description':'test',
    'title':'test',
    'subtitle':'test',
    'series':'test',
    'volume':'test',
    'ready_for_sale':True,
    'publisher':'3',
    'primary_author':'Preston',
    'other_authors':'stephen, mitchell',
}

response = requests.get("http://127.0.0.1:8000/store/books/ingest"+filepath)
print(response.content)
 
#insert mitchell's function for dictionaries
#for loop on the dictionary doing posts
response = requests.put("http://127.0.0.1:8000/store/books/process", data=book)
# response = requests.post("http://127.0.0.1:8000/store/books/process")
