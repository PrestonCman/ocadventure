import json

class SiteBookData():           #SiteBookData Class
    def __init__(self):
        pass



class book_site():
    def __init__(self, slug):
        with open('parsers.json') as parserList:
            parsers = json.load(parserList)
    
        self.slug = slug
        self.parser = parsers[slug]
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
        pass



def Get_book_site(slug):
    """Function that takes a string and returns a booksite url"""
    return book_site(slug)