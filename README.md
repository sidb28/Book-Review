# CS50 Project 1 : Book Review
## Website deployed to https://whispering-sierra-16856.herokuapp.com/ 

### Description
A simple book review website built using Flask, Heroku and the Goodreads API. The system is able to register and authenticate users, and query for books by title, author or ISBN. Users may also view reviews by others and/or leave one themselves. This system has been built keeping in mind the requirements of Project 1 for Harvard's CS50 Web Programming. 

### For local development
- Clone this repository
- ``` pip install -r requirements.txt ```
- ``` cd <name of folder> ```
- Set environment variables:
    - FLASK_APP = application.py
    - DATABASE_URL
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
    
