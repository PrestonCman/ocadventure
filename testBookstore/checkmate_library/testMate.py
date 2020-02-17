"""
This file is for testing any functions you wish to invoke from the checkmate library
"""


from Checkmate import *

site = Get_book_site("amazon-books/b?ie=UTF8&node=132")
print(site.slug)
print(site.Siteurl)
print(site.parser)