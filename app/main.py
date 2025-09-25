from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import auth, customers, credit_check

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CRMock API",
    description="A mock CRM API for testing purposes",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(credit_check.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to CRMock API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}