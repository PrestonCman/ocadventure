import json
import io
from lxml import etree
import requests
from urllib.parse import urlparse, parse_qs
from PIL import Image
import mechanize
import re

class site_book_data():
    def __init__(self,content):
        self.content = content
        
        self.book_dictionary = { 
            'format' : None, 
            'book_title' : None, 
            'book_image' : None,
            'book_image_url' : None,
            'isbn_13' : None, 
            'description' : None, 
            'series' : None, 
            'volume_number' : None, 
            'subtitle' : None, 
            'authors' : None, 
            'book_id' : None,
            'site_slug' : None,
            'parse_status' : "FULLY_PARSED",
            'url' : None,
            #'content' : self.content,
            'ready_for_sale' : False,
            'extra' : None,
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
            query = parse_qs(parsed.query)
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

    def parse_LC(self, parser, url, root):
        """
            Parsing function for Livraria Cultura eBook store.  Given a parser JSON
            object and the url of the book to be parsed, will return a parsed site book data object
        """

        self.book_dictionary["book_id"] = self.parse_id_from_url(url, 36, len(url)-2)
        self.book_dictionary["extra"] = parser["extra"]

        try:
            for key in parser:
                if key == "format" or key == "site_url" or key == "extra" or parser[key] == "!Not_Reachable":
                    pass
                    #not parsable or readable content
                else:
                    parsed = root.xpath(parser[key])
                    if len(parsed) != 0:
                        if key == "book_image":
                            self.get_book_image(parsed[0], key)
                        elif key == "authors":
                            authors = parsed[0].split("|")
                            parsedAuthors = []
                            for author in authors:
                                parsedAuthors.append(author[6:len(author)-1])
                            self.book_dictionary[key] = parsedAuthors
                        elif key == "ready_for_sale":
                            self.book_dictionary[key] = True
                        else:
                            self.book_dictionary[key] = parsed[0]
        except:
            # if failed, the site book data object will be given a parsed value of "Failed"
            self.book_dictionary["parse_status"] = "UNSUCCESSFUL"
        
        return self

    def parse_SD(self, parser, url, root):
        
        myUrl = urlparse(url)
        self.book_dictionary[key] = self.parse_id_from_url(url, (myUrl.path.find("k")+2), myUrl.path.rfind("/"))
        self.book_dictionary["ready_for_sale"] = True
        self.book_dictionary["extra"] = parser["extra"]

        try:
            for key in parser:
                if parser[key] == "!Not_Reachable" or key == "site_url" or key == "extra":
                    pass
                    #not parsable/readable content
                else:
                    parsed = root.xpath(parser[key])
                    if len(parsed) != 0:
                        if key == "format":
                            self.book_dictionary[key] = parsed[-1].text
                        elif key == "description" or key == "book_image_url":
                            self.book_dictionary[key] = parsed[0]
                        elif key == "book_image":
                            self.get_book_image(parsed[0], key)
                        else:
                            p = []
                            for elem in parsed:
                                p.append(elem.text)
                            self.book_dictionary[key] = p
                            #parse as normal
        except:
            self.book_dictionary["parse_status"] = "UNSUCCESSFUL"

        return self
    
    def parse_KB(self, parser, url, root):

        myUrl = urlparse(url)
        end = myUrl.path.rfind("/")
        self.book_dictionary["book_id"] = myUrl.path[end+1:]
        self.book_dictionary["extra"] = parser["extra"]

        try:
            for key in parser:
                if (parser[key] == "!Not_Reachable" or key == "extra" or key == "site_url"):
                    pass
                    #not parsable/readable content
                else:
                    parsed = root.xpath(parser[key])
                    if len(parsed) > 0:
                        if key == "format":
                            book_format = parsed[0][:parsed[0].find(" Details")]
                            if book_format == "eBook":
                                self.book_dictionary[key] = "DIGITAL"
                            elif book_format == "Audiobook":
                                self.book_dictionary[key] = "AUDIOBOOK"
                        elif key == "book_title" or key == "subtitle":
                            parsed = parsed[0].strip("\r\n")
                            self.book_dictionary[key] = parsed
                        elif key == "description":
                            description = ""
                            for element in parsed:
                                description += element
                            self.book_dictionary[key] = description
                        elif (key == "book_image"):
                            self.get_book_image("http:" + parsed[0], key)
                        elif (key == "isbn_13"):
                            for element in parsed:
                                if element.text == "ISBN: ":
                                    isbn = element.xpath("./span")
                                    self.book_dictionary[key] = isbn[0].text
                        elif (key == "authors"):
                            authors = []
                            for author in parsed:
                                authors.append(author.text)
                            self.book_dictionary[key] = authors
                        elif (key == "ready_for_sale"):
                            self.book_dictionary[key] = True
                        else:
                            parsed = parsed[0].strip("\r\n")
                            self.book_dictionary[key] = parsed
        except:
            self.book_dictionary["parse_status"] = "UNSUCCESSFUL"

        return self

    def parse_TB(self,parser,url, root):
        parse = etree.HTMLParser(remove_pis=True)
        tree = etree.parse(io.BytesIO(self.content),parse)
        root = tree.getroot()
        try:
            self.book_dictionary["format"] = "test book"

            title_element = root.xpath(parser["book_title"])[0]
            self.book_dictionary["book_title"] = title_element.text

            isbn_element = root.xpath(parser["isbn_13"])
            self.book_dictionary["isbn_13"] = isbn_element

            description_element = root.xpath(parser["description"])
            self.book_dictionary["description"] = description_element

            authors = list()
            authors.append(root.xpath(parser["authors"]))
            self.book_dictionary["authors"] = authors

            series_element = root.xpath(parser["series"])
            if len(series_element) == 0:
                self.book_dictionary["series"] = None 
            else:
                self.book_dictionary["series"] = series_element
                
            volume_element = root.xpath(parser["volume_number"])
            if len(volume_element) == 0:
                self.book_dictionary["volume_number"] = None
            else:
                self.book_dictionary["volume_number"] = volume_element

            self.book_dictionary["book_id"] = url[35: len(url)-1]
            self.book_dictionary["site_slug"] = "TB"
            self.book_dictionary["url"] = url
            ready_element = root.xpath(parser["ready_for_sale"])
            if ('not' in str(ready_element)) :
                self.book_dictionary["ready_for_sale"] = False
            else:
                self.book_dictionary["ready_for_sale"] = True

        except:
            # if failed, the site book data object will be given a parsed value of "Failed"
            self.book_dictionary["parse_status"] = "UNSUCCESSFUL"

        return self

    def get_book_image(self, image_url, key):
        resp = requests.get(image_url, stream=True).raw
        self.book_dictionary[key] = Image.open(resp)

    def parse_id_from_url(self, url, start, end):
        id = url[start: end]
        return id

    def __str__(self):
        msg = ""
        for key in self.book_dictionary:
            if(str(key) != "book_image"):
                msg += key + " : " + str(self.book_dictionary[key]) + "\n"
        return msg

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
        book_data.book_dictionary["site_slug"] = self.slug
        book_data.book_dictionary["url"] = url

        temp_parse = etree.HTMLParser(remove_pis=True)
        tree=etree.parse(io.BytesIO(content),temp_parse)
        root=tree.getroot()

        if self.slug == "GB":
            return book_data.parse_GB(self.parser, url)
        elif(self.slug == "SD"):
            return book_data.parse_SD(self.parser, url, root)
        elif(self.slug == "LC"):
            return book_data.parse_LC(self.parser, url, root)
        elif (self.slug == "KB"):
            return book_data.parse_KB(self.parser, url, root)
        elif (self.slug == "TB"):
            return book_data.parse_TB(self.parser, url, root)

    def find_book_matches_at_site(self, book_data):
        """Given a sitebookData object, search for the book 
        at the 'book_site' site and provide a list of likely 
        matches paired with how good of a match it is (1.0 is an 
        exact match). This should take into account all the info 
        we have about a book, including the cover."""

        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Chrome')]
        if self.slug == 'TB':
            br.open(self.site_url)
            br.select_form(nr=1)
            control = br.form.find_control('q')
        elif self.slug == 'KB':
            br.open(self.site_url)
            br.select_form(nr=0)
            control = br.form.find_control('query')
        elif self.slug == 'GB':
            url = 'https://books.google.com'
            br.select_form(nr=0)
            control = br.form.find_control('q')
        elif self.slug == 'SD':
            url = 'https://www.scribd.com/books'
            br.open(url)
            br.select_form(nr=0)
            control = br.form.find_control('query')
        elif self.slug == 'LC':
            url = 'https://wwwe.livrariacultura.com.br/'
            br.select_form(nr=0)
            control = br.form.find_control(nr=0)



        query = ""
        if self.slug == 'TB':
            if book_data.book_dictionary["isbn_13"] is not None:
                query += book_data.book_dictionary["isbn_13"]
            elif book_data.book_dictionary["book_title"] is not None:
                query += book_data.book_dictionary["book_title"]
            elif book_data.book_dictionary["authors"] is not None:
                query += book_data.book_dictionary["authors"][0]
            #query = book_data.book_dictionary["authors"][0]
            #For testing purposes of multiple books in query
        else:   
            if book_data.book_dictionary['book_title'] is not None:
                query += book_data.book_dictionary['book_title'] + ' '
            if book_data.book_dictionary['isbn_13'] is not None:
                query += book_data.book_dictionary['isbn_13'] + ' '
            if book_data.book_dictionary['authors'] is not None:
                query += book_data.book_dictionary['authors'][0] + ' '
        control.value = query
        response = br.submit()
        #print(response.read()) #this gives the raw html.
        #print(response.geturl()) #gives the full url of the query so it's easier to read than the raw html. good for parsing.
        #must parse the response to give the list of books
        num_books = 50
        book_list = self.parse_response(num_books, response.geturl())
        #now take results and assign them a value for how likely a match they are.
        return book_list

    def parse_response(self, num_books, url):
        """parse book results into a list of books to return."""

        book_list = []
        query_finished = False
        while not query_finished:

            content = requests.get(url).content
            temp_parse = etree.HTMLParser(remove_pis=True)
            tree=etree.parse(io.BytesIO(content),temp_parse)
            root=tree.getroot()

        #use lxml queries to get the book results and then use a loop to append each book in the results to the list. use book_list.append()
            if self.slug == 'TB':
                books = root.xpath("//ul[@id='search_result']//a/@href")
                for book in books:
                    book_url = self.site_url + book
                    book_list.append(self.get_book_data_from_site(book_url))

                if len(book_list) < num_books:
                    if len(root.xpath("//span[@class='page-links']//a[text()='next']"))==0:
                        query_finished = True
                        break
                    else:
                        current_page = root.xpath("//span[@class='page-current']")[0]
                        next_page = current_page.xpath("./following-sibling::a[1]/@href")[0]
                        next_page = next_page.replace(" ", "+")
                        url= self.site_url + "/store/search/" + next_page
                elif len(book_list) >= num_books:
                    del book_list[num_books:]
                    query_finished = True
            
            elif self.slug == 'KB':
                books = root.xpath("//div[@class='item-detail']/a/@href")
                for book in books:
                    book_url = self.site_url + book
                    book_list.append(self.get_book_data_from_site(book_url))

                if len(book_list) < num_books:
                    if len(root.xpath("//a[@class='page-link final active']")) > 0:
                        query_finished = True
                        break
                        #reached the end of book results found from query
                    else:
                        current_page = root.xpath("//a[@class='page-link first active' or @class='page-link reveal active' or @class='page-link active']")[0]
                        next_page = current_page.xpath("./following-sibling::a[1]/@href")[0]
                        url = self.site_url + next_page

                elif len(book_list) >= num_books:
                    del book_list[num_books:]
                    query_finished = True
                
            elif self.slug == 'GB':
                pass

            elif self.slug == 'SD':
                myQuery = "//script[12]"
                parsed = root.xpath(myQuery)
                results = parsed[0].text
                bookIds = parse_scribd_json_for_ids(results)
                bookURLS = []
                for ID in bookIds:
                    bookURLS.append(self.convert_book_id_to_url(ID))

                testLoad = mechanize.Browser()
                testLoad.set_handle_robots(False)
                testLoad.addheaders = [('User-agent', 'Chrome')]
                for book in bookURLS:
                    response = testLoad.open(book)
                    url = response.geturl()
                    if(url[23] == 'b' or url[23] == 'a'):
                        book_list.append(self.get_book_data_from_site(book))
                    if(len(book_list) == num_books):
                        break
                query_finished = True
            
            elif self.slug == 'LC':
                pass

        return book_list

    def convert_book_id_to_url(self, book_id):
        """given a book_id, return the direct url for the book."""
        
        if self.slug == "LC":
            url = self.site_url + book_id + "/p"
        
        elif self.slug == "KB":
            if requests.get(self.site_url + "/us/en/ebook/" + book_id).status_code == 200:
                url = self.site_url + "/us/en/ebook/" + book_id
            else:
                url = self.site_url + "/us/en/audiobook/" + book_id
        
        elif self.slug =="TB":
            url = self.site_url  + "/store/search/" + book_id
        
        elif self.slug =="SD":
            if requests.get(self.site_url + "book/" + book_id).status_code == 200:
                url = self.site_url + "book/" + book_id + "/"
            else:
                url = self.site_url + "audiobook/" + book_id + "/"

        else:
            url = self.site_url + book_id

        return url

def get_book_site(slug):
    """Function that takes a string and returns a booksite url"""
    
    return book_site(slug)

def parse_scribd_json_for_ids(results):
    ids = [m.start() for m in re.finditer('"doc_id":', results)]
    bookIds = []
    start = int(ids[-1]) + 9
    end = start + 9
    counter = 0
    for i in ids:
        start = int(ids[counter]) + 9
        end = start + 9
        bookIds.append(results[start:end])
        counter += 1
    return bookIds
    


    

