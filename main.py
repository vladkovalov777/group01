from fastapi import FastAPI, status, HTTPException, Query
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime
from fastapi.templating import Jinja2Templates
from storage import storage
from fastapi import Request

app = FastAPI(
    title="Book store 📚 5897",
    debug=True,
)
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    books = storage.get_books()
    context = {"request": request, "books": books}
    return templates.TemplateResponse("index.html", context=context)


class NewBookSchema(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100,
        examples=["Кінематографічні роздуми Квентіна Тарантіно"],
    )
    description: str = Field(
        max_length=15000,
        examples=[
            "Тарантіно — унікальний випадок у кінематографі. Хлопчик, закоханий у кіно, що пройшов доволі нетривіальний, як на голлівудського режисера, шлях (за його власними словами, «я не ходив у кіношколу, я ходив у кіно»). Його творчість не вкладається у сталі жанрові рамки, він ніколи не тяжів до лінійності сюжету, і ця книга не виняток."
        ],
    )
    price: float = Field(gt=0)
    image: str


class BookPk(BaseModel):
    pk: str


class BookFull(NewBookSchema, BookPk):
    created_at: datetime


# api
# CREATE
@app.post("/api/books/create", status_code=status.HTTP_201_CREATED)
def create_book(new_book: NewBookSchema) -> BookPk:
    new_book_dict = new_book.dict()
    new_book_dict["pk"] = uuid4().hex
    new_book_dict["created_at"] = datetime.now()
    storage.create(new_book_dict)
    return new_book_dict


# READ
@app.get("/api/books/{pk}")
def get_book(pk: str) -> BookFull:
    book = storage.get_book(pk)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return book


@app.get("/api/books")
def get_books(
    q: str = "",
    limit: int = Query(default=10, gt=0, le=50),
    max_price: float = Query(default=5000000, gt=0, le=5000000),
) -> list[BookFull]:
    return storage.get_books(q=q, limit=limit, max_price=max_price)


@app.patch("/api/books/{pk}")
def patch_book_image(pk: str, image: str) -> BookPk:
    book = storage.get_book(pk)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    storage.patch_book_image(pk, image)
    return book


@app.put("/api/books/{pk}")
def put_book(pk: str, book: NewBookSchema) -> BookFull:
    stored_book = storage.get_book(pk)
    if not stored_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    storage.update_book(pk, book.dict())
    updated_book = storage.get_book(pk)
    return updated_book


@app.delete("/api/books/{pk}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(pk: str):
    storage.delete_book(pk)


# web
