# CS50 Project 1 : Book Review
## Website deployed to https://whispering-sierra-16856.herokuapp.com/ 

### Description
A simple book review website built using Flask, Heroku and the Goodreads API. The system is able to register and authenticate users, and query for books by title, author or ISBN. Users may also view reviews by others and/or leave one themselves. This system has been built keeping in mind the requirements of Project 1 for Harvard's CS50 Web Programming. 

### Usage
- Clone this repository
- ``` pip install -r requirements.txt ```
- ``` cd <name of folder> ```
- Set environment variables:
    - FLASK_APP = application.py
    - DATABASE_URL = postgres://nnelpbcsjduspm:0a196be33e89142509f375bb70fe917fab70d5895175da6b33ddcc0b919fde06@ec2-18-210-214-86.compute-1.amazonaws.com:5432/da9ckvt5agbpgj
    - (optional) FLASK_DEBUG = 1
- ``` flask run ```

### API Calls to the System
An API call to the route /api/<isbn> returns a json as follows(example below):
```
{
  "author": "Jennifer Weiner", 
  "average_score": 3.0, 
  "isbn": "0743294270", 
  "review_count": 3, 
  "title": "Fly Away Home", 
  "year": 2010
}
```

#### The files included in this repository are as follows:
- application.py - Main controller of the system
- templates folder - Contains html views for the different pages
- static - Contains the stylesheet for the system
- books.csv - CSV file with data of 5000 books
- import.py - Script to create tables in database and import values from books.csv into books table
- authenticator.py - Helper script for authenticating users before feature access

