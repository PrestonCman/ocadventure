"""
This file is for testing any functions you wish to invoke from the checkmate library
"""
from Checkmate import *
import io
from lxml import etree
import requests
from time import process_time

def parser_TB_test():
    print("Testing Test Bookstore Site: \n")
    urls = ["32",
    "50",
    "4075",
    "6",
    "519",
    "1396",
    "3940",
    "712",
    "1728",
    "5000"]
    site = book_site("TB")
    try:
        for url in urls:
            url = site.convert_book_id_to_url(url)
            site_book_data = site.get_book_data_from_site(url)
            print(site_book_data)
        print("\n Successfully parsed! \n")
    except Exception as e:
        print("\n Parsing Failed \n")
        print(e)
        print(e.args)
def parser_KB_test():
    print("Testing Kobo Site: \n")
    urls = ["dragon-s-code",
    "the-tattooist-of-auschwitz-3",
    "these-ghosts-are-family-1",
    "the-berenstain-bears-thanksgiving",
    "the-outsider-58",
    "the-night-watchman-11",
    "witchmark",
    "the-forgotten-home-child-1",
    "when-we-were-vikings-1",
    "deadpool-kills-the-marvel-universe"]
    site = book_site("KB")

    try:
        for url in urls:
            url = site.convert_book_id_to_url(url)
            site_book_data = site.get_book_data_from_site(url)
            print(site_book_data)
        print("\n Successfully parsed! \n")
    except Exception as e:
        print("\n Parsing Failed \n")
        print(e)
        print(e.args)

def parser_GB_test():
    print("Testing Google Books Site: \n")
    urls = ["6_pSpWuCrakC",
    "tcSMCwAAQBAJ",
    "DKcWE3WXoj8C",
    "LxSfNHOFKfUC",
    "RriuDwAAQBAJ",
    "lFhbDwAAQBAJ",
    "SQIbAAAAYAAJ",
    "VtffjwEACAAJ",
    "mo2fehxBgxYC",
    "3Wdh6YGXOxMC"]
    site = book_site("GB")
    try:
        for url in urls:
            url = site.convert_book_id_to_url(url)
            site_book_data = site.get_book_data_from_site(url)
            print(site_book_data)
        print("\n Successfully parsed! \n")
    except Exception as e:
        print("\n Parsing Failed \n")
        print(e)
        print(e.args)

def parser_SD_test():
    print("Testing Scrib D Site: \n")
    urls = ["170477477",
    "170472413",
    "395188529",
    "249308926",
    "237913032",
    "402030445",
    "237584449",
    "445384013",
    "401824729",
    "409612764"]
    site = book_site("SD")
    try:
        for url in urls:
            url = site.convert_book_id_to_url(url)
            site_book_data = site.get_book_data_from_site(url)
            print(site_book_data)
        print("\n Successfully parsed! \n")
    except Exception as e:
        print("\n Parsing Failed \n")
        print(e)
        print(e.args)

def parser_LC_test():
    print("Testing Livraria Cultura Site: \n")
    urls = ["berenstain-bears-thank-god-for-good-health-111826738", 
    "seu-signo-em-2020-peixes-2012851444", 
    "a-misteriosa-estatua-de-um-anjo-2012279894",
    "my-name-is-prince-2112135828",
    "era-uma-vez-tres-historias-de-enrolar-17868632", 
    "raul-da-ferrugem-azul-17559469", 
    "intermediate-guide-to-ceramic-glazing-layer-2012820506", 
    "transformando-palavras-em-dinheiro-2012987076", 
    "frame-up-the-111414035", 
    "revolucao-das-plantas-2012370492"]
    site = book_site("LC")
    try:
        for url in urls:
            url = site.convert_book_id_to_url(url)
            site_book_data = site.get_book_data_from_site(url)
            print(site_book_data)
        print("\n Successfully parsed! \n")
    except Exception as e:
        print("\n Parsing Failed \n")
        print(e)
        print(e.args)

def id_to_url_test():
    id = "1"
    site = book_site("TB")
    print("\nTest Bookstore book url from ID "+ id + "\nBook URL: " + site.convert_book_id_to_url(id))

    id = "dragon-s-code"
    site = book_site("KB")
    print("\nKobo Bookstore book url from ID "+ id + "\nBook URL: " + site.convert_book_id_to_url(id))

    id = "6_pSpWuCrakC"
    site = book_site("GB")
    print("\nGoogle Bookstore book url from ID "+ id + "\nBook URL: " + site.convert_book_id_to_url(id))

    id = "170477477"
    site = book_site("SD")
    print("\nScrib D Bookstore book url from ID "+ id + "\nBook URL: " + site.convert_book_id_to_url(id))

    id = "berenstain-bears-thank-god-for-good-health-111826738"
    site = book_site("LC")
    print("\nLivraria Cultura Bookstore book url from ID " + id + "\nBook URL: " + site.convert_book_id_to_url(id))

def main():
    try:
        parser_TB_test()
        parser_KB_test()
        parser_GB_test()
        parser_SD_test()
        parser_LC_test()
        id_to_url_test()
        print("\n Test(s) were successful \n")
    except Exception as e:
        print("\n Test(s) Failed \n")
        print(e)
        print(e.args)

main()
