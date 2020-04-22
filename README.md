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

Navigating the Repo:

Directories for Major Processes and Test Functions throughout Project:

Test Bookstore
ROOT DIRECTORY: testBookstore/store

    Major Process           Location        Line of Code
    ----------------------------------------------------
    process onix            views.py             33
    upload onix             views.py            120
	
    Test Function	    Location	    Line of Code
    ----------------------------------------------------
    upload new onix         tests.py              5
    
	
Checkmate Library
ROOT DIRECTORY: checkmate_library

    Major Process           Location        Line of Code
    ----------------------------------------------------
    html parser paths       parsers.json          1
    handle parser data      Checkmate.py         14
    find book matches       Checkmate.py        350
    parse book matches      Checkmate.py        405
    rank book matches       Checkmate.py        484

    Test Functions          Location        Line of Code
    ----------------------------------------------------
    bookstore parsers       testMate.py          11
    convert id to url       testMate.py         132
    find book matches       testMate.py         153
    scrap testBookstore     testMate.py         163


Business 2 Business Site
ROOT DIRECTORY: b2b/b2bsite

    Major Process           Location        Line of Code
    ----------------------------------------------------
    search bookstores       views.py             25

    Test Functions          Location        Line of Code
    ----------------------------------------------------
    book query              tests.py             10


For both the Test Bookstore and Business 2 Business Site, you may need to run the migration commands
by performing the following in SEQUENTIAL ORDER
    'python manage.py makemigrations'
    'python manage.py migrate'

    Ensure you have navigated to the correct directory from the base oc_adventure folder
    by performing the following commands
    For Test Bookstore - cd testBookstore
    For Business 2 Business Site - cd b2b

If migrations are up to date then you are ready to run the Test Bookstore or Business 2 Business site

To run the test bookstore, cd into testBookstore and execute the 'python manage.py runserver' command.

Parsers for checkmate library are in parsers.Json. To add a parser, add the site slug with all the xpath queries as sub objects of the slug.

The site scraper functions are all located in Checkmate.py in the site_book_data() class. 

To test Checkmate.py, make sure the test bookstore is running and then cd into /testBookstore/checkmate_library and run 'python testMate.py'.

To test the Business 2 Business site, cd into b2b and execute the 'python manage.py runserver' command

 Default Admin Login for Test Bookstore and Business 2 Business Site:
    Username - admin
    Password - password
