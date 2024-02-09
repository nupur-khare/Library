from fastapi import FastAPI

from api.app.routers import fetch_books, auth, add_books, delete_books
from api.models import Response

app = FastAPI()


@app.get("/", response_model=Response)
def index():
    return {"message": "hello"}


app.include_router(delete_books.router, prefix="/api/delete", tags=["Delete Books"])
app.include_router(add_books.router, prefix="/api/add", tags=["Add Books"])
app.include_router(fetch_books.router, prefix="/api/fetch", tags=["Fetch Books"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
