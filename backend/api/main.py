from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.config.db import create_db_and_tables
from api.routers import quote
from api.config.seed_data import seed_database

origins = [
    "http://localhost:3000",  # Local Frontend
    "http://localhost:8080",  # Vue.js dev server
    "http://quotes.local",    # Kubernetes domain
    "http://quotes.local:*",  # Any port on the Kubernetes domain
    "http://127.0.0.1:*",     # Localhost with any port
    "http://localhost:*",      # Localhost with any port
    "*"  # ⚠️ Just for development, remove in production
    ]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the database and tables at startup
    # SQLModel.metadata.create_all(engine)
    create_db_and_tables()
    seed_database()
    yield
    # Optionally, you can drop the tables at shutdown
    # SQLModel.metadata.drop_all(engine)

app = FastAPI(
    title="Quotes API",
    description="Simple Quote API",
    root_path="/api",
    docs_url="/docs",           #  /api/docs
    redoc_url="/redoc",         #  /api/redoc
    openapi_url="/openapi.json", #  /api/openapi.json
    openapi_tags=[{
        "name": "quotes",
        "description": "quotes endpoints"
    }],
    lifespan=lifespan
)
app.include_router(quote.router)

# CORS configuration
# Allow requests from specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST", 
        "PUT",
        "DELETE",
        "OPTIONS"
    ],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "User-Agent",
        "X-Requested-With",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
)

@app.get("/")
async def root():
    return {"quote": "May the force be with you!"}

