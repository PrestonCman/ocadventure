"""
This file is for testing any functions you wish to invoke from the checkmate library
"""


from Checkmate import *
import json 

# site = get_book_site("amazon-books/b?ie=UTF8&node=132")
site = get_book_site("TB")
site_book_data = site.get_book_data_from_site("http://127.0.0.1:8000/store/search/3822/")
print(site_book_data.book_dictionary)
# book2 = get_book_data_from_site("https://www3.livrariacultura.com.br/espirito-e-letra-2012794543/p")
# print(site.slug)
# print(site.parser)




