import os, csv
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
  try:
    db.execute( "CREATE TABLE books (id SERIAL PRIMARY KEY, title VARCHAR(50) NOT NULL, author VARCHAR(50) NOT NULL, isbn VARCHAR(10) NOT NULL UNIQUE, year INT NOT NULL )" )
    db.execute( "CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR(50) NOT NULL, password VARCHAR(50) NOT NULL)" )
    db.execute("CREATE TABLE reviews (id SERIAL PRIMARY KEY, user_id INT REFERENCES users(id) ON DELETE CASCADE, book_id INT REFERENCES books(id) ON DELETE CASCADE, rating INT NOT NULL, description TEXT) ")

    print("Tables created in database!")

    with open('books.csv', newline='') as csvfile:
      booksreader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
      next(booksreader, None)
      for book in booksreader:
        db.execute("INSERT INTO books (title, author, isbn, year) VALUES (:title, :author, :isbn, :year)",{"title": book[1], "author": book[2], "isbn": book[0], "year": book[3]})

        print(f"{book[1]} successfully added!")    
    db.commit()
    print("Import from books.csv complete!")
  except:
    print("Import Failed. Please try again!")

if __name__ == "__main__":
  main()