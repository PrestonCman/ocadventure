from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from .models import Book
from django.db.models import Q
from .serializers import BookSerializer
from rest_framework import generics

def home(request):
    return render(request, 'store/home.html')

def bookDetail(request, book_id):
    context = {
        'book' : get_object_or_404(Book, pk = book_id)
    }
    return render(request, 'store/bookDetail.html', context)

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

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer