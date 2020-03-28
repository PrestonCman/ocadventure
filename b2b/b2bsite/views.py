from django.shortcuts import render


def home(request):
    return render(request, 'b2b/home.html')


''' Not done yet :)
def login(request):
    return render(request, 'regristration/login.html')
'''