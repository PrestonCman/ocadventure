from django.test import TestCase
import requests
# Create your tests here.

filepath = {
     "filepath":"/Users/preston/Documents/Programs/teamproject/testBookstore/store/idiot.txt"
}

response = requests.get("http://127.0.0.1:8000/store/books/process", filepath)

response = requests.get("http://127.0.0.1:8000/store/books/process")
print(response.content)
 
# response = requests.post("http://127.0.0.1:8000/store/books/process")
