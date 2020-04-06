class Parser:
    def __init__(self, content):
        self.attributes = { 
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
            'parse_status' : "Fully Parsed",
            'url' : None,
            'content' : self.content,
            'ready_for_sale' : None,
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

    def parse_LC(self, parser, url):
        """Parsing function for Livraria Cultura eBook store.  Given a parser JSON
        object and the url of the book to be parsed, will return a parsed site book data object"""
        temp_parse=etree.HTMLParser(remove_pis=True)
        tree=etree.parse(io.BytesIO(self.content),temp_parse)
        root=tree.getroot()

        #tries to parse all information from given book url
        try:
            self.book_dictionary["format"] = "ebook"

            parsed = root.xpath(parser["book_title"])
            if len(parsed) != 0:
                self.book_dictionary["book_title"] = parsed[0]

            parsed = root.xpath(parser["book_image_url"])
            if len(parsed) != 0:
                self.book_dictionary["book_image_url"] = parsed[0]
                resp = requests.get(parsed[0], stream=True).raw
                self.book_dictionary["book_image"] = Image.open(resp)   

            parsed = root.xpath(parser["isbn_13"])
            if len(parsed) != 0:
                self.book_dictionary["isbn_13"] = parsed[0]

            parsed = root.xpath(parser["description"])
            if len(parsed) != 0:
                self.book_dictionary["description"] = parsed[0]

            self.book_dictionary["book_id"] = self.parse_id_from_url(url, 36, len(url)-2)

            parsed = root.xpath(parser["authors"])
            if len(parsed) != 0:
                authors = parsed[0].split("|")
                parsedAuthors = []
                for author in authors:
                    parsedAuthors.append(author[6:len(author)-1])
                
                self.book_dictionary["authors"] = parsedAuthors

            parsed = root.xpath(parser["ready_for_sale"])
            if len(parsed) != 0:
                self.book_dictionary["ready_for_sale"] = True
            else:
                self.book_dictionary["ready_for_sale"] = False

            self.book_dictionary["site_slug"] = "LC"
            self.book_dictionary["url"] = parser["site_url"]
            self.book_dictionary["parse_status"] = "Success"
        except:
            # if failed, the site book data object will be given a parsed value of "Failed"
            self.book_dictionary["parse_status"] = "Failed"
        
        return self

    def parse_SD(self, parser, url):
        self.book_dictionary["site_slug"] = "SD"
        self.book_dictionary["url"] = url
        temp_parse = etree.HTMLParser(remove_pis=True)
        tree=etree.parse(io.BytesIO(self.content),temp_parse)
        root=tree.getroot()
        for key in parser:
            try:
                if(parser[key] == "!Not_Reachable" or key == "site_url"):
                    pass
                    #not parsable/readable content
                elif(key == "format"):
                    parsed = root.xpath(parser[key])
                    self.book_dictionary[key] = parsed[-1].text
                elif(key == "description" or key == "book_image_url"):
                    parsed = root.xpath(parser[key])
                    self.book_dictionary[key] = parsed[0]
                elif(key == "book_image"):
                    resp = requests.get(self.book_dictionary["book_image_url"], stream=True).raw
                    self.book_dictionary[key] = Image.open(resp)
                elif(key == "book_id"):
                    myUrl = urlparse(url)
                    self.book_dictionary[key] = self.parse_id_from_url(myUrl.path, (myUrl.path.find("k")+2), myUrl.path.rfind("/"))
                    #parse url for bookID
                elif(key == "extra"):
                    self.book_dictionary[key] = parser[key]
                        #call any functions for additionaly queries here
                else:
                    parsed = root.xpath(parser[key])
                    p = []
                    for elem in parsed:
                        p.append(elem.text)
                    self.book_dictionary[key] = p
                    #parse as normal
            except:
                    self.book_dictionary["parse_status"] = "Unsuccessful"
        return self
    
    def parse_KB(self, parser, url):
        self.book_dictionary["site_slug"] = "KB"
        self.book_dictionary["url"] = url
        temp_parse = etree.HTMLParser(remove_pis=True)
        tree=etree.parse(io.BytesIO(self.content),temp_parse)
        root=tree.getroot()
        for key in parser:
            try:
                if (parser[key] == "!Not_Reachable" or key == "site_url"):
                    pass
                    #not parsable/readable content
                elif (key == "format"):
                    parsed = root.xpath(parser[key])[0].text
                    parsed = parsed[:parsed.find(" Details")]
                    if parsed == "eBook":
                        self.book_dictionary[key] = "DIGITAL"
                    elif parsed == "Audiobook":
                        self.book_dictionary[key] = "AUDIOBOOK"
                elif (key == "book_title" or key == "subtitle"):
                    parsed = root.xpath(parser[key])
                    if len(parsed) > 0:
                        parsed = parsed[0].text.strip("\r\n")
                        self.book_dictionary[key] = parsed
                    else:
                        self.book_dictionary[key] = None
                        #Book does not have a subtitle
                elif (key == "book_image_url"):
                    parsed = root.xpath(parser[key])
                    self.book_dictionary[key] = parsed[0]
                elif (key == "book_image"):
                    resp = requests.get("http:" + self.book_dictionary["book_image_url"], stream=True).raw
                    self.book_dictionary[key] = Image.open(resp)
                elif (key == "isbn_13"):
                    parsed = root.xpath(parser[key])
                    for element in parsed:
                        if element.text == "ISBN: ":
                            isbn = element.xpath("./span")
                            self.book_dictionary[key] = isbn[0].text
                elif (key == "description"):
                    parsed = root.xpath(parser[key])
                    description = ""
                    for element in parsed:
                        description += element
                    self.book_dictionary[key] = description
                elif (key == "book_id"):
                    myUrl = urlparse(url)
                    end = myUrl.path.rfind('/')
                    self.book_dictionary[key] = myUrl.path[end+1:]
                elif (key == "authors"):
                    parsed = root.xpath(parser[key])
                    authors = []
                    for author in parsed:
                        authors.append(author.text)
                    self.book_dictionary[key] = authors
                elif (key == "series"):
                    parsed = root.xpath(parser[key])
                    if len(parsed) > 0:
                        self.book_dictionary[key] = parsed[0].text
                    else:
                        self.book_dictionary[key] = None
                        #Book not included in series
                elif (key == "ready_for_sale"):
                    if len(root.xpath(parser[key])) > 0:
                        self.book_dictionary[key] = True
                    else:
                        self.book_dictionary[key] = False
                elif (key == "extra"):
                    self.book_dictionary[key] = parser[key]
                else:
                    self.book_dictionary[key] = root.xpath(parser[key])[0].text
            except:
                self.book_dictionary["parse_status"] = "UNSUCCESSFUL"
                break
            
        if self.book_dictionary["parse_status"] != "UNSUCCESSFUL":
            self.book_dictionary["parse_status"] = "PARSE_SUCCESSFUL"

        return self
    
    def parse_id_from_url(self, url, start, end):
        id = url[start: end]
        return id

    def parse_TB(self,parser,url):
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

            self.book_dictionary["parse_status"] = "Success"
        except:
            # if failed, the site book data object will be given a parsed value of "Failed"
            self.book_dictionary["parse_status"] = "Failed"
        return self


    def __str__(self):
        for key in self.attributes:
            print key + " : " + self.attributes[key] + "\n"

        return msg