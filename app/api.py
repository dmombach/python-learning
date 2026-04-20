from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db import create_db_and_tables
from .routes import contacts, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (optional cleanup)
    # e.g., close connecrtions, flush logs, etc.


app = FastAPI(lifespan=lifespan)

app.include_router(contacts.router)
app.include_router(auth.router)
