import io
from lxml import etree
import requests

class SiteBookData():           #SiteBookData Class
    def __init__(self):
        pass



class book_site():
    def __init__(self, slug):
        pass

        url = {
            #slug : (url, parser)
            "TB" : None, #test bookstore
            "KB" : None,  #Kobo
            "GB" : None, #Google Books
            "SD" : None, #Scribd
            "LC" : None #Lavraria
        }

        self.slug = slug
        self.parser = parsers[slug]
        self.site_url = self.parser["site-url"]
        #pass queries to self.parser

    def get_book_data_from_site(self, url):
        """Given a string URL to a book page at a site, 
        parse it and return the siteBookData of the info"""
        
        pass

    def find_book_matches_at_site(self, book_data):
        """Given a sitebookData object, search for the book 
        at the 'book_site' site and provide a list of likely 
        matches paired with how good of a match it is (1.0 is an 
        exact match). This should take into account all the info 
        we have about a book, including the cover."""

        pass

    def convert_book_id_to_url(self, book_id):
        """given a book_id, return the direct url for the book."""
        url = self.site_url + self.book_id
        if self.slug == "LC":
            url += "/p"
        return url



def get_book_site(slug):
    """Function that takes a string and returns a booksite url"""
    
    return book_site(slug)