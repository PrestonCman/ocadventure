from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('search/request/', views.searchAPI.as_view()),
    path('results/', views.do_search, name='results'),
