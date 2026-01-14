"""
Database configuration and session management
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment or default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agent_notes.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class Note(Base):
    """Note model for storing user notes"""
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    tags = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize database on import
if __name__ != "__main__":
    try:
        init_db()
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")
