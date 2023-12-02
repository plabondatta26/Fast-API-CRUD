from fastapi import FastAPI, HTTPException, Depends, APIRouter
from core.database import Session_Local, get_db
from sqlalchemy.orm import Session
from models import book as book_model
from schema.book_schema import BookCreateSchema, BookSchema

router = APIRouter()


@router.get('/books/', response_model=list[BookSchema], tags=['Books'])
def get_books(db: Session = Depends(get_db)):
    return db.query(book_model.Books).all()


# add book into database
@router.post('/books/', tags=['Books'])
def create_book(book: BookCreateSchema, db: Session = Depends(get_db)):
    book_obj = book_model.Books()
    book_obj.title = book.title
    book_obj.author = book.author
    book_obj.description = book.description
    book_obj.rating = book.rating
    db.add(book_obj)
    db.commit()
    return book


@router.get('/books/{book_id}/', tags=['Books'], response_model=BookSchema)
def retrieve_book(book_id: int, db: Session_Local = Depends(get_db)):
    book_obj = db.query(book_model.Books).filter(book_model.Books.id == book_id).first()
    if book_obj:
        return book_obj
    else:
        raise HTTPException(
            status_code=404,
            detail="Book does not found"
        )


@router.put('/books/{book_id}/', tags=['Books'])
def update_book(book_id: int, book: BookCreateSchema, db: Session_Local = Depends(get_db)):
    book_obj = db.query(book_model.Books).filter(book_model.Books.id == book_id).first()
    if book_obj:
        book_obj.title = book.title
        book_obj.author = book.author
        book_obj.description = book.description
        book_obj.rating = book.rating
        db.add(book_obj)
        db.commit()
        return book
    else:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )


@router.delete('/books/{book_id}/', tags=['Books'])
def delete_book(book_id: int, db: Session_Local = Depends(get_db)):
    book_obj = db.query(book_model.Books).filter(book_model.Books.id == book_id).first()
    if book_obj:
        db.query(book_model.Books).filter(book_model.Books.id == book_id).delete()
        db.commit()
        return {"detail": f"Book successfully deleted"}
    else:
        raise HTTPException(status_code=200, detail="Book not found")
