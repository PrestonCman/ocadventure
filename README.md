# ocadventure
Team project SEV

Dependencies:

Django 2.2.7
lxml   4.5.0
mechanize 0.4.5
Pillow 7.0.0
Pygments 2.5.2
requests 2.22.0
sqlparse 0.3.0
urllib3 1.25.8

Test bookstore is located in the store folder. 
To run the test bookstore, cd into testBookstore and execute the python manage.py runserver command.

Parsers for checkmate library are in parsers.Json. To add a parser, add the site slug with all the xpath queries as sub objects of the slug.

The site scraper functions are all located in Checkmate.py in the site_book_data() class. 

To test Checkmate.py, make sure the test bookstore is running and then cd into /testBookstore/checkmate_library and run the testMate.py file.
