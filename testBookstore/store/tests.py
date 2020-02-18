from django.test import TestCase
import requests
# Create your tests here.

filepath = "/Users/preston/Documents/Programs/teamproject/testBookstore/store/tests.py"

response = requests.get('http://127.0.0.1:8000/store/books/ingest/', {'filepath': filepath}) 
print(response)
# response = requests.put("http://127.0.0.1:8000/store/books/process")
 
