from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from data_access.database import engine, Base
from controllers import hotel_controller

# Це автоматично створить таблиці в MySQL, якщо їх там ще немає
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lab 3 - MVC Booking App")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Підключаємо контролер
app.include_router(hotel_controller.router)

# Головна сторінка просто перекидає на /hotels/
@app.get("/")
def root():
    return RedirectResponse(url="/hotels/")