from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Employee as emp


import sys
sys.path.append('..\\checkmate_library\\')
from Checkmate import *


@login_required
def home(request):
    return render(request, 'b2b/home.html')

@login_required
def search(request):
    return render(request, 'b2b/search.html')

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
    
    #s = b.get_book_data_from_site("https://www.scribd.com/book/401824729/Maybe-You-Should-Talk-to-Someone-A-Therapist-HER-Therapist-and-Our-Lives-Revealed")
    #bookList = [[1.0, s], [0.5, s]]

    return render(request, 'b2b/results.html', {'book_list': bookList})

''' Not done yet :)
def login(request):
    return render(request, 'regristration/login.html')
'''
