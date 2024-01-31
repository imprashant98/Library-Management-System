from fastapi import FastAPI
from Books.api import router as books_router
from config.db_config import SessionLocal


app = FastAPI()
app.include_router(books_router)
# app.include_router(items.router)


@app.get("/")
async def root():
    return {"message": "Library MS Created"}
