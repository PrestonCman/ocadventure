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

Test bookstore processes found in testBookstore/store
    Major Process           Location
    onix process            views.py
    onix upload             views.py
    


To run the test bookstore, cd into testBookstore and execute the python manage.py runserver command.

Parsers for checkmate library are in parsers.Json. To add a parser, add the site slug with all the xpath queries as sub objects of the slug.

The site scraper functions are all located in Checkmate.py in the site_book_data() class. 

To test Checkmate.py, make sure the test bookstore is running and then cd into /testBookstore/checkmate_library and run the testMate.py file.

Business 2 Business Site:
 - Default Admin Login:
        Username - admin
        Password - password

 Explains how to navigate the repo…what major functionality is located where
o Describes which functionality has unit tests written for it (and where those tests are
located)
o How to install/test. You aren’t literally explaining how to install a production
environment, but it needs to describe everything necessary to set up a functioning dev
environment (just as if a new programmer were coming on your team and they needed
to spin up quickly). This includes things like database setup and configuration scripts,
what we need to do to set up a virtual environment, etc. You need to put some time
into this and have multiple team members read through it…if it is poorly written and
unclear it will significantly impact this portion of your grade.