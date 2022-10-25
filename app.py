from fastapi import FastAPI, APIRouter
from url import router as urls_router

app = FastAPI()

app.include_router(urls_router, prefix="")

