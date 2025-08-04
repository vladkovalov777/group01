from fastapi import FastAPI, Request, HTTPException, status, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
from storage import storage

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class Tour(BaseModel):
    title: str
    description: str
    price: float
    image: str


class TourPk(BaseModel):
    pk: str


class TourFull(Tour, TourPk):
    created_at: datetime


@app.post("/api/tours/create")
def create_tour(tour: Tour):
    tour_dict = tour.dict()
    tour_dict["pk"] = uuid4().hex
    tour_dict["created_at"] = datetime.now()
    storage.create(tour_dict)
    return {"pk": tour_dict["pk"]}


@app.get("/api/tours")
def get_tours(
    q: str = "", limit: int = 20, max_price: float = 999999
) -> list[TourFull]:
    print(storage.get_tours(q, limit, max_price))
    return storage.get_tours(q, limit, max_price)


@app.get("/api/tours/{pk}")
def get_tour(pk: str) -> TourFull:
    tour = storage.get_tour(pk)
    if not tour:
        raise HTTPException(status_code=404, detail="Not found")
    return tour


@app.put("/api/tours/{pk}")
def update_tour(pk: str, tour: Tour):
    if not storage.get_tour(pk):
        raise HTTPException(status_code=404)
    storage.update_tour(pk, tour.dict())
    return storage.get_tour(pk)


@app.delete("/api/tours/{pk}")
def delete_tour(pk: str):
    storage.delete_tour(pk)


@app.get("/", response_class=HTMLResponse)
def home(request: Request, q: str = ""):
    tours = storage.get_tours(q)
    return templates.TemplateResponse(
        "index.html", {"request": request, "tours": tours}
    )


@app.get("/tour/{pk}", response_class=HTMLResponse)
def detail(request: Request, pk: str):
    tour = storage.get_tour(pk)
    if not tour:
        return RedirectResponse("/")
    return templates.TemplateResponse(
        "tour_detail.html", {"request": request, "tour": tour}
    )
