from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'b2b/home.html')
    return render(request, 'b2b/home.html')

def search(request):
    return render(request, 'b2b/search.html')

def do_search(request):
    return render(request, 'b2b/results.html')

''' Not done yet :)
def login(request):
    return render(request, 'regristration/login.html')
'''
