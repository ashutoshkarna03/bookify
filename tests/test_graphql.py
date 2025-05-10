import pytest
from app.main import app
from starlette.testclient import TestClient
from app.models import Author, Book
from sqlalchemy.orm import Session

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_graphql_books_query(client, db_session: Session):
    # Create test data
    author = Author(name="Test Author", bio="Test Bio")
    db_session.add(author)
    db_session.commit()
    
    book = Book(title="Test Book", description="Test Description", author_id=author.id)
    db_session.add(book)
    db_session.commit()

    query = '{ books { id title description author { id name } } }'
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "books" in data["data"]
    books = data["data"]["books"]
    assert len(books) > 0
    assert books[0]["title"] == "Test Book"
    assert books[0]["author"]["name"] == "Test Author"

def test_create_author_and_book(client, db_session: Session):
    # Create an author
    mutation_author = '''
    mutation {
      createAuthor(name: "Test Author", bio: "Bio") {
        id
        name
        bio
      }
    }
    '''
    response = client.post("/graphql", json={"query": mutation_author})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "createAuthor" in data["data"]
    author = data["data"]["createAuthor"]
    assert author["name"] == "Test Author"
    author_id = author["id"]

    # Create a book for that author
    mutation_book = f'''
    mutation {{
      createBook(title: "Test Book", authorId: {author_id}, description: "A test book") {{
        id
        title
        description
        author {{ id name }}
      }}
    }}
    '''
    response = client.post("/graphql", json={"query": mutation_book})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "createBook" in data["data"]
    book = data["data"]["createBook"]
    assert book["title"] == "Test Book"
    assert book["author"]["id"] == author_id

    # Query the book
    query = '{ books { id title description author { id name } } }'
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "books" in data["data"]
    books = data["data"]["books"]
    assert len(books) > 0
    assert any(b["title"] == "Test Book" for b in books) 