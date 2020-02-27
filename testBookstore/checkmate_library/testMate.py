"""
This file is for testing any functions you wish to invoke from the checkmate library
"""


from Checkmate import *
import io
from lxml import etree
import requests
from time import process_time

urls = ["https://www.scribd.com/book/249308926/1984", "https://www.scribd.com/book/322011391/The-Subtle-Art-of-Not-Giving-a-F-ck-A-Counterintuitive-Approach-to-Living-a-Good-Life", "https://www.scribd.com/book/262747675/A-Wrinkle-in-Time-The-Graphic-Novel", "https://www.scribd.com/book/249307564/The-Fellowship-of-the-Ring-Being-the-First-Part-of-The-Lord-of-the-Rings"]


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
    query = "//script"
    for url in urls:
        content = fetch(url)
        try:
            parse(content, query)
        except Exception as e:
            print("Error on  : " + url)
            print(type(e))
            print(e.args)
            print(e)


main()

