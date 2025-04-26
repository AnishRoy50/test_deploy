from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://*.vercel.app"],  # Local and Vercel domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define models
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

# Pydantic model for request/response
class ItemCreate(BaseModel):
    name: str

class ItemResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items")
def read_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return items

@app.post("/items")
def create_item(item: ItemCreate):
    db = SessionLocal()
    db_item = Item(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return db_item
