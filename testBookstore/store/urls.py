from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search.as_view(), name='search'),
    path('search/<int:book_id>/', views.bookDetail, name = 'detail'),
    path('books/', views.BookList.as_view()),
    path('books/<int:pk>/', views.BookDetail.as_view()),
]