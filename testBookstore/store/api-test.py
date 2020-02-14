import requests

onix_file = ""

def ingest(file_name):
    onix_file = file_name
    return "\nName of ingested file: " + onix_file

def process():
    return_response = ""
    if(onix_file == ""):
        print("No file specified")
    else:
        print("Processing files")
        #for each book in the file specified
            #get the info for the book and store in a python dictonary
            #response = requests.post(_url('/store/books/ingest/'), json=dictonary you created)
            #if the response.status_code is a bad error code, add it to a dictionary of error books with the code
        #if dict of error books is empty, set return_response = "all books processes successfully" 
        #else set return_response = error books dictonary.
    return return_response

def _url(path):
    return 'https://127.0.0.1:8000' + path
    
ingest_response = ingest("onix3_example.xml")
print(ingest_response)