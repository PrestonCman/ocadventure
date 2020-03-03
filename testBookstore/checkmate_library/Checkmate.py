import io
import json
from lxml import etree
import requests
from urllib.parse import urlparse, parse_qs
from PIL import Image


class site_book_data():
    def __init__(self,content):
        self.content = content
      
    
    #In this dictionary it doesnt have "extra"
        self.book_dictionary = { 
            'format' : None, 
            'book_title' : None, 
            'isbn_13' : None, 
            'description' : None, 
            'series' : None, 
            'volume_number' : None, 
            'subtitle' : None, 
            'authors' : None, 
            'site_slug' : None,
            'book_id' : None, 
            'url' : None,
            'ready_for_sale' : None,
            'book_image' : None,
            }

    def parse_GB(self, parser, url):
            temp_parse = etree.HTMLParser(remove_pis=True)
            tree=etree.parse(io.BytesIO(self.content),temp_parse)
            root=tree.getroot()

            parsed = root.xpath(parser["book_title"])
            if len(parsed) != 0:
                self.book_dictionary["book_title"] = parsed[0].text

            parsed = root.xpath(parser["isbn_13"])
            if len(parsed) != 0:
                isbn = str.split(parsed[0].text, ', ')
                self.book_dictionary["isbn_13"] = isbn[1]

            parsed = root.xpath(parser["book_image_url"])
            if len(parsed) != 0:
                self.book_dictionary["book_image_url"] = parsed[0]
                response = requests.get(parsed[0], stream=True).raw
                self.book_dictionary["book_image"] = Image.open(response)
                

            parsed = root.xpath(parser["description"])
            if len(parsed) != 0:
                self.book_dictionary["description"] = parsed[0]
            else:
                parsed = root.xpath(".//div[@id='synopsistext']/text()")
                if len(parsed) != 0:
                    self.book_dictionary["description"] = parsed[0]

            parsed = root.xpath(parser["authors"])
            authors = list()
            if len(parsed) != 0:
                for author in parsed:
                    authors.append(author.text)
                self.book_dictionary["authors"] = authors

            self.book_dictionary["site_slug"] = "GB"
            self.book_dictionary["url"] = url

            parsed = urlparse(url)
            #print(parsed)
            query = parse_qs(parsed.query)
            #print(query)
            self.book_dictionary["book_id"] = query["id"][0]
            
            parsed = root.xpath(parser["ready_for_sale"])
            if len(parsed) != 0:
                if parsed[0] == 'No eBook available':
                    self.book_dictionary["ready_for_sale"] = False
                    self.book_dictionary["format"] = "Print"
            else:
                self.book_dictionary["ready_for_sale"] = True
                self.book_dictionary["format"] = "eBook" 

            return self


    def parse_SD(self, parser, url):
        self.book_dictionary["site_slug"] = "SD"
        self.book_dictionary["url"] = url
        temp_parse = etree.HTMLParser(remove_pis=True)
        tree=etree.parse(io.BytesIO(self.content),temp_parse)
        root=tree.getroot()
        for key in parser:
                if(parser[key] == "!Not_Reachable"):
                    pass
                    #not parsable/readable content
                elif(key == "description" or key == "book_image_url"):
                    parsed = root.xpath(parser[key])
                    self.book_dictionary[key] = parsed[0]
                elif(key == "book_image"):
                    resp = requests.get(self.book_dictionary["book_image_url"], stream=True).raw
                    self.book_dictionary[key] = Image.open(resp)
                elif(key == "book_id"):
                    myUrl = urlparse(url)
                    end = myUrl.path.rfind('/')
                    self.book_dictionary[key] = myUrl.path[6:end]
                    #parse url for bookID
                elif(key == "site_url"):
                    self.book_dictionary[key] = parser[key]
                    #immediately hand over site url
                elif(key == "extra"):
                    for extraKey in parser[key]:
                        query = parser[key][extraKey]
                        #call any functions for additionaly queries here
                else:
                    parsed = root.xpath(parser[key])
                    p = []
                    for elem in parsed:
                        p.append(elem.text)
                    self.book_dictionary[key] = p
                    #parse as normal
        return self


class book_site():
    def __init__(self, slug):
        with open("parsers.json") as parserList:
            parsers = json.load(parserList)

        self.slug = slug
        self.parser = parsers[slug]
        self.site_url = self.parser["site_url"]
        #pass queries to self.parser

    def get_book_data_from_site(self, url):
        """Given a string URL to a book page at a site, 
        parse it and return the siteBookData of the info"""

        content = requests.get(url).content

        book_data = site_book_data(content)
        if self.slug == "GB":
            book_data = site_book_data(content)
            return book_data.parse_GB(self.parser, url)
        elif(self.slug == "SD"):
            book_data.parse_SD(self.parser, url)
            return book_data.parse_SD(self.parser, url)

    

    def find_book_matches_at_site(self, book_data):
        """Given a sitebookData object, search for the book 
        at the 'book_site' site and provide a list of likely 
        matches paired with how good of a match it is (1.0 is an 
        exact match). This should take into account all the info 
        we have about a book, including the cover."""

        pass

    def convert_book_id_to_url(self, book_id):
        """given a book_id, return the direct url for the book."""
        url = self.site_url + book_id
        if self.slug == "LC":
            url += "/p"
        return url



def get_book_site(slug):
    """Function that takes a string and returns a booksite url"""
    
    return book_site(slug)

