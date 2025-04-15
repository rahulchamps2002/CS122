from sqlalchemy import Column, Integer, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer)
    price = Column(Float)

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}', year={self.year}, price={self.price})>"


engine  = create_engine('sqlite:///books.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_book(title, author, year, price):
    book = Book(title=title, author=author, year=year, price=price)
    session.add(book)
    session.commit()
    session.refresh(book)
    return "Booked Added Successfully!"

def get_all_books():
    books = session.query(Book).all()

def edit_book(book_id, title, author, year, price):
    book = session.query(Book).filter_by(id=book_id).first()
    if not book:
        return "Book ID not found!"
    book.title = title
    book.author = author
    book.year = year
    book.price = price
    session.commit()
    return "Book updated successfully!"

def delete_book(book_id):
    book = session.query(Book).filter_by(id=book_id).first()
    if not book:
        return "Book ID not found!"
    session.delete(book)
    session.commit()
    return "Book deleted successfully!"

