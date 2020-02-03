from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Book
from django.db.models import Q

def home(request):
    return render(request, 'store/home.html')

class search(ListView):
    model = Book
    template_name = 'store/search.html'

    #q is the name given to the user input, object list is the resulting query set after checking 
    #all the books if ISBN, primary author, other authors, or title contains the user query.
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(Q(title__icontains=query) | Q(primary_author__icontains=query) |
                                          Q(other_authors__icontains=query) | Q(isbn_13__icontains=query))
        print(object_list)      #remove this later when html list display is added.  
        return object_list

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['query'] = self.request.GET.get('q')
        return data