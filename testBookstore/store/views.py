from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from .models import Book, LastONIXFile
from django.db.models import Q
from .serializers import BookSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import HttpResponse

from lxml import etree

onix_file = ""

def home(request):
    return render(request, 'store/home.html')

def bookDetail(request, book_id):
    context = {
        'book' : get_object_or_404(Book, pk = book_id)
    }
    return render(request, 'store/bookDetail.html', context)

def openFile(xmlfile):
    with open(xmlfile, 'rb') as fobj:
        xml = fobj.read()
    return etree.fromstring(xml)

def ONIXsearch(root, query):
    return root.xpath(query)

def processONIX(fileName):
    root = openFile(fileName)


    book = {
        "isbn_13" : None,
        "price" : None,
        "description" : None,
        "title" : None,
        "subtitle": None,
        "series" : None,
        "volume" : None,
        "ready_for_sale" : None,
        "publisher" : None,
        "primary_author" : None,
        "other_authors" : None,
    }




    books = []
    
    queries = {
        "title" : "Product/DescriptiveDetail[Language/LanguageCode = 'eng']/TitleDetail[TitleType = '01']/TitleElement[TitleElementLevel = '01']/TitleText",
        "isbn_13" : "Product[DescriptiveDetail/Language/LanguageCode = 'eng']/ProductIdentifier[ProductIDType ='15']/IDValue",                          
        "description" : "Product[DescriptiveDetail/Language/LanguageCode = 'eng']/CollateralDetail/TextContent[TextType = '03']/Text",          
        "price" : "Product[DescriptiveDetail/Language/LanguageCode = 'eng']/ProductSupply/SupplyDetail/Price[not(PriceQualifier)]/PriceAmount",
        "primary_author" : "Product/DescriptiveDetail[Language/LanguageCode = 'eng']/Contributor[SequenceNumber = '1']/PersonName",
        "ready_for_sale" : "Product[DescriptiveDetail/Language/LanguageCode = 'eng']/PublishingDetail/PublishingStatus", #not final value
        "publisher" : "Product[DescriptiveDetail/Language/LanguageCode = 'eng']/PublishingDetail/Publisher/PublisherName",
        }

    numberBooks = len(ONIXsearch(root, "//Product[DescriptiveDetail/Language/LanguageCode = 'eng']"))                    #Retrieve the Total number of books from the file

    for i in range(numberBooks):
        books.append(book.copy())                               #Create that many book dictionaries


    for query in queries:                                       #Go through all the queries
        results = ONIXsearch(root, queries[query])                  #Get everything I know isthere
        for i in range(len(books)):                          
            books[i][query] = results[i].text                   #set element of book dictionary equal to retrieved value


    for book in books:
        if(book["ready_for_sale"] == '04'):
            book["ready_for_sale"] = True
        elif(book["ready_for_sale"] == '07'):
            book["ready_for_sale"] = False
        else:
            books.remove(book)

    for book in books:
        isbn = book["isbn_13"]
        subtitle = "Product[ProductIdentifier/IDValue = " + str(isbn) + "]/DescriptiveDetail/TitleDetail/TitleElement/Subtitle"
        try:
            results = ONIXsearch(root, subtitle)[0]
            book["subtitle"] = results.text
        except:
            book["subtitle"] = results.text

        series = "Product[ProductIdentifier/IDValue = " + str(isbn) + "]/DescriptiveDetail/Collection/TitleDetail/TitleElement/TitleText"
        try:
            results = ONIXsearch(root, series)[0]
            book["bookseries"] = results.text
        except:
            book["bookseries"] = None


        authors = ONIXsearch(root, "Product[ProductIdentifier/IDValue = " + str(isbn) + "]/DescriptiveDetail/Contributor/PersonName")
        book["primary_author"] = authors[0].text
        if(len(authors) != 1):
            buffer = ""
            for i in range(1, len(authors)):
                if(i != 1):
                    buffer += ", "
                buffer += authors[i].text
            book["other_authors"] = buffer


        volume = ONIXsearch(root, "Product[ProductIdentifier/IDValue = " + str(isbn) + "]/DescriptiveDetail/Collection/TitleDetail/TitleElement/PartNumber")
        if(len(volume) != 0):
            book["volume"] = volume[0].text

        return books

def postBooks(books):
    serializer_class = BookSerializer
    invalid_books = []
    for book in books:
        bookData = BookSerializer(data=book)
        print("Posting...")
        try:
            existingBook = Book.objects.get(isbn_13=book["isbn_13"])

            existingBook.isbn_13 = book["isbn_13"]
            existingBook.price = book["price"]
            existingBook.description = book["description"]
            existingBook.title = book["title"]
            existingBook.subtitle = book["subtitle"]
            existingBook.series = book["series"]
            existingBook.volume = book["volume"]
            existingBook.ready_for_sale = book["ready_for_sale"]
            existingBook.publisher = book["publisher"]
            existingBook.primary_author = book["primary_author"]
            existingBook.other_authors = book["other_authors"]
             
            existingBook.save()
        except:
            if bookData.is_valid():
                bookData.save()
            else:
                invalid_books.append(book)
    return invalid_books

       
class search(ListView):
    model = Book
    template_name = 'store/search.html'
    paginate_by = 5

    #q is the name given to the user input, object list is the resulting query set after checking 
    #all the books if ISBN, primary author, other authors, or title contains the user query.
    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Book.objects.filter(Q(title__icontains=query) | Q(primary_author__icontains=query) |
                                          Q(other_authors__icontains=query) | Q(isbn_13__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['query'] = self.request.GET.get('q')
        return data

class ProcessBook(APIView):
    serializer_class = BookSerializer

    def get(self, request):      
        try:
            onix_file = self.request.query_params["filepath"]
            fileSave = LastONIXFile.objects.get()
            fileSave.file_path = onix_file
            fileSave.save()
        except:
            onix_file = self.request.query_params["filepath"]
            fileSave = LastONIXFile(file_path=onix_file)
            fileSave.save()
            onix_file = fileSave.file_path
        return HttpResponse(onix_file)
        
    def put(self, request):
        response = "Books added successfully"
        invalid_books = postBooks(processONIX(LastONIXFile.objects.get().file_path))
        if(len(invalid_books) != 0):
            response = "Error: Some books were invalid, check console for more information"
            for i in invalid_books:
                print(i)

        return HttpResponse(response)
    

