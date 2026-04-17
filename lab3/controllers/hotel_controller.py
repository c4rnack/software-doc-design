from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from data_access.database import get_db
from services.hotel_service import HotelService

router = APIRouter(prefix="/hotels")
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def list_hotels(request: Request, db: Session = Depends(get_db)):
    hotels = HotelService.get_all_hotels(db)
    return templates.TemplateResponse(request=request, name="hotels/list.html", context={"request": request, "hotels": hotels})

@router.post("/add")
def add_hotel(
    name: str = Form(...),
    description: str = Form(""),
    contactEmail: str = Form(""),
    country: str = Form("Ukraine"), # Нове поле
    city: str = Form(...),          # Нове поле
    street: str = Form(...),        # Нове поле
    number: str = Form(...),        # Нове поле
    db: Session = Depends(get_db)
):
    # Передаємо всі параметри в сервіс
    HotelService.create_hotel(db, name, description, contactEmail, country, city, street, number)
    return RedirectResponse(url="/hotels/", status_code=303)

@router.post("/{hotel_id}/edit")
def edit_hotel_submit(
    hotel_id: int,
    name: str = Form(...),
    description: str = Form(""),
    contactEmail: str = Form(""),
    country: str = Form(...),
    city: str = Form(...),
    street: str = Form(...),
    number: str = Form(...),
    db: Session = Depends(get_db)
):
    HotelService.update_hotel(db, hotel_id, name, description, contactEmail, country, city, street, number)
    return RedirectResponse(url="/hotels/", status_code=303)

# --- НОВІ МАРШРУТИ ---

# Маршрут для видалення готелю
@router.post("/{hotel_id}/delete")
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    HotelService.delete_hotel(db, hotel_id)
    return RedirectResponse(url="/hotels/", status_code=303)

# Маршрут для відображення сторінки редагування
@router.get("/{hotel_id}/edit", response_class=HTMLResponse)
def edit_hotel_page(request: Request, hotel_id: int, db: Session = Depends(get_db)):
    hotel = HotelService.get_hotel(db, hotel_id)
    return templates.TemplateResponse(request=request, name="hotels/edit.html", context={"request": request, "hotel": hotel})
