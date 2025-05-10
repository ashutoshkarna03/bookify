import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Book as BookModel, Author as AuthorModel

@strawberry.type
class Author:
    id: int
    name: str
    bio: Optional[str] = None
    books: List['Book']

@strawberry.type
class Book:
    id: int
    title: str
    description: Optional[str] = None
    author: Author

@strawberry.type
class Query:
    @strawberry.field
    def books(self) -> List[Book]:
        db = next(get_db())
        books = db.query(BookModel).all()
        return books

    @strawberry.field
    def book(self, id: int) -> Optional[Book]:
        db = next(get_db())
        return db.query(BookModel).filter(BookModel.id == id).first()

    @strawberry.field
    def authors(self) -> List[Author]:
        db = next(get_db())
        authors = db.query(AuthorModel).all()
        return authors

    @strawberry.field
    def author(self, id: int) -> Optional[Author]:
        db = next(get_db())
        return db.query(AuthorModel).filter(AuthorModel.id == id).first()

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_author(self, name: str, bio: Optional[str] = None) -> Author:
        db = next(get_db())
        author = AuthorModel(name=name, bio=bio)
        db.add(author)
        db.commit()
        db.refresh(author)
        return author

    @strawberry.mutation
    def create_book(self, title: str, author_id: int, description: Optional[str] = None) -> Book:
        db = next(get_db())
        book = BookModel(title=title, author_id=author_id, description=description)
        db.add(book)
        db.commit()
        db.refresh(book)
        return book

schema = strawberry.Schema(query=Query, mutation=Mutation) 