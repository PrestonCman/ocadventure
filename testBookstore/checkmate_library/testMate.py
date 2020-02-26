"""
This file is for testing any functions you wish to invoke from the checkmate library
"""


from Checkmate import *
import io
from lxml import etree
import requests

urls = ["https://www.scribd.com/book/249308926/1984", "https://www.scribd.com/book/322011391/The-Subtle-Art-of-Not-Giving-a-F-ck-A-Counterintuitive-Approach-to-Living-a-Good-Life", "https://www.scribd.com/book/262747675/A-Wrinkle-in-Time-The-Graphic-Novel"]


def fetch(url):
    response = requests.get(url)
    return response.content



def parse(content, query):
    parser = etree.HTMLParser(remove_pis=True)
    tree=etree.parse(io.BytesIO(content),parser)
    root=tree.getroot()

    parsed = root.xpath(query)
    print(len(parsed))
    return parsed[0].text


def main():
    #query = "//span[@itemprop='author']/a"
    #query = "//td[@class = 'line-content']/following-sibling"
    ##query = "//tr/td[@class='line-content']/span[@class='html-attribute-value']"
    query = "//span[@class='meta_label'][3]/span[2]"#[span = 'ISBN: ']"
    for url in urls:
        content = fetch(url)
        try:
            print(parse(content, query))
        except Exception as e:
            print("Error on  : " + url)
            print(type(e))
            print(e.args)
            print(e)



main()

