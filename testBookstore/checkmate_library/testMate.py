"""
This file is for testing any functions you wish to invoke from the checkmate library
"""
import io
import json
from lxml import etree
import requests
from PIL import Image
from Checkmate import *
from time import process_time

urls = ["https://www.scribd.com/book/249308926/1984", "https://www.scribd.com/book/322011391/The-Subtle-Art-of-Not-Giving-a-F-ck-A-Counterintuitive-Approach-to-Living-a-Good-Life", "https://www.scribd.com/book/262747675/A-Wrinkle-in-Time-The-Graphic-Novel", "https://www.scribd.com/book/249307564/The-Fellowship-of-the-Ring-Being-the-First-Part-of-The-Lord-of-the-Rings"]

# import mechanize

# site = get_book_site("amazon-books/b?ie=UTF8&node=132")
site2 = get_book_site("LC")
# book2 = get_book_data_from_site("https://www3.livrariacultura.com.br/espirito-e-letra-2012794543/p")
# print(site.slug)
# print(site.parser)

print(site2.slug)
print("Specific Book url by ID")
url1 = site2.convert_book_id_to_url("10-receitas-tipicas-de-minas-gerais-2012330937")
print(site2.convert_book_id_to_url("10-receitas-tipicas-de-minas-gerais-2012330937"))
print("parser")
print(site2.parser)

def fetch(url):
    response = requests.get(url)
    return response.content



def parse(content, query):
    parser = etree.HTMLParser(remove_pis=True)
    tree=etree.parse(io.BytesIO(content),parser)
    root=tree.getroot()

    parsed = root.xpath(query)
    print(len(parsed))
    #print(parsed)
    for text in parsed:
        print(text.text)

def main():
    site = book_site("LC")
    site_book_data = site.get_book_data_from_site("https://www3.livrariacultura.com.br/as-mentiras-mais-contadas-e-que-todo-mundo-2012250588/p")
    print(site_book_data.book_dictionary)
        
main()

# def main():

#     # br = mechanize.Browser("https://www3.livrariacultura.com.br")
#     # br.open("https://www3.livrariacultura.com.br")
#     urls = ["https://www3.livrariacultura.com.br/as-mentiras-mais-contadas-e-que-todo-mundo-2012250588/p",
#     "https://www3.livrariacultura.com.br/galaxia-humana-em-in-plosao-2012944846/p",
#     "https://www3.livrariacultura.com.br/a-gota-2011370114/p"]
#     query = "//button[@class='buy-in-page-button']"
#     for url in urls:
#         content = fetch(url)
#         try:
#             parse(content, query)

#         except Exception as e:
#             print("Error on  : " + url)
#             print(type(e))
#             print(e.args)
#             print(e)


# main()
