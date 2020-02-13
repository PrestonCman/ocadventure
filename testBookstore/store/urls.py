from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search.as_view(), name='search'),
    path('search/<int:book_id>/', views.bookDetail, name = 'detail'),
    path('books/process', views.ProcessBook.as_view()),
    path('books/ingest', views.IngestBook.as_view()),
]