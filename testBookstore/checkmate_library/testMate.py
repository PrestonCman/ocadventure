"""
This file is for testing any functions you wish to invoke from the checkmate library
"""


from Checkmate import *

# site = get_book_site("amazon-books/b?ie=UTF8&node=132")
site2 = get_book_site("LC")
# book2 = get_book_data_from_site("https://www3.livrariacultura.com.br/espirito-e-letra-2012794543/p")
# print(site.slug)
# print(site.parser)

print(site2.slug)
print("Specific Book url by ID")
print(site2.convert_book_id_to_url("10-receitas-tipicas-de-minas-gerais-2012330937"))
print("parser")
print(site2.parser)