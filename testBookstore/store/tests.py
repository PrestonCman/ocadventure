from django.test import TestCase
import requests
# Create your tests here.

filepath = "store/20190110Update_stripped.xml"

response = requests.post('http://127.0.0.1:8000/store/books/ingest/', {'filepath': filepath}) 
print(response)
response = requests.put("http://127.0.0.1:8000/store/books/process")
print("done") 
