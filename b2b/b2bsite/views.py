from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'b2b/home.html')
    
@login_required
def search(request):
    return render(request, 'b2b/search.html')
