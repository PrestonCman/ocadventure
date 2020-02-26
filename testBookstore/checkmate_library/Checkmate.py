class SiteBookData():
    def __init__(self,content):
        self.content = content
      
    
    #In this dictionary it doesnt have "extra"
        self.bookDictionary = { 'book_format' : None, 'book_title' : None, 'isbn_13' : None, 'description' : None, 'series' : None, 'volume_number' : None, 'subtitle' : None, 'authors' : None, 'site_slug' : None,
        'book_id' : None, 'url' : None, 'ready_for_sale' : None}

    #Here we need to give the value to dictionary. USing the parser.
    #for key in dictionary:
     #   key = getInfo(key)



class book_site():
    def __init__(self, slug):
        pass

        url = {
            #slug : (url, parser)
            "amazon-books/b?ie=UTF8&node=132" : ("https://www.amazon.com/amazon-books/b?ie=UTF8&node=13270229011", None)        #Not Final
        }

        self.slug = slug
        self.Siteurl = url[slug][0]
        self.parser = url[slug][1]

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