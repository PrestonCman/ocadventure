from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from .models import Employee, Company
from django.http import HttpResponse

import sys
sys.path.append('../checkmate_library/')
sys.path.append('../checkmate_library/parsers.json')

from Checkmate import *

@login_required
def home(request):
    return render(request, 'b2b/home.html')

@login_required
def search(request):
    return render(request, 'b2b/search.html')

@login_required
def do_search(request):
    u = request.user.username
    user = User.objects.get(username = u)
    e = emp.objects.get(user = user)
    num = e.num_queries
    num += 1
    e.num_queries = num
    e.save()

    book_isbn = request.GET.get("isbn_field")
    book_title = request.GET.get("title_field")
    book_authors_raw = request.GET.get("author_field").split(",")
    book_authors_final = []
    for author in book_authors_raw:
        book_authors_final.append(author.strip(" "))

    b = book_site("KB")
    bookList = []

    tempBook = site_book_data(None)
    if(book_isbn != ""):
        tempBook.book_dictionary['isbn_13'] = book_isbn
    else:
        tempBook.book_dictionary['isbn_13'] = None

    if(book_title != ""):
        tempBook.book_dictionary['book_title'] = book_title    
    else:
        tempBook.book_dictionary['book_title'] =  None


    if(len(book_authors_final) != 0):
        tempBook.book_dictionary['authors'] = book_authors_final
    else:
        tempBook.book_dictionary['authors'] = None


    bookList = b.find_book_matches_at_site(tempBook)
    

    return render(request, 'b2b/results.html', {'book_list': bookList})

class searchAPI(APIView):
    def post(self, request):
        """
        Given a request searches multiple sites for book matches
        """      
        #this will retrieve the sites for the user
        request_query = self.request.POST.get("query")
        query = self.string_to_site_book_data_dictionary(request_query)
        slugs = ["KB"]
        for slug in slugs:
            site = book_site(slug)
            print(site.find_book_matches_at_site(query))
        #num_queries = self.request.POST.get("num_queries")+1
        #num_queries.save()

        return HttpResponse()
    
    def string_to_site_book_data_dictionary(self, query):
        """
        Converts the text query from the request into a site book data object
        """
        site_book = site_book_data(None)
        seperated_query = query.splitlines()
        book_dict = {}
        for s in seperated_query:
            value = s.split(":")
            if value[0].rstrip(" ") == "ready_for_sale":
                if value[1].lstrip(" ") == "True":
                    book_dict[value[0].rstrip(" ")] = True
                else:
                    book_dict[value[0].rstrip(" ")] = False
            else:
                if value[1].lstrip(" ") == "None":
                    book_dict[value[0].rstrip(" ")] = None
                else:
                    book_dict[value[0].rstrip(" ")] = value[1].lstrip(" ")
    
        book_dict["book_image"] = None
        site_book.book_dictionary = book_dict
        #print(site_book.book_dictionary)
        return site_book

