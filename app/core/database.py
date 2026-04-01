import os
import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# 1. Create the Engine (The "Heart" of the connection)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# 2. Create a Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# app/core/database.py

def update_journal_analysis(journal_id: str, analysis_json: dict):
    db = SessionLocal()
    try:
        # We use "journals" (lowercase) because of your @@map("journals")
        query = text('UPDATE journals SET analysis = :analysis WHERE id = :id')
        
        result = db.execute(query, {
            "analysis": json.dumps(analysis_json),
            "id": journal_id
        })
        
        db.commit()
        
        if result.rowcount > 0:
            print(f"--- [SQLAlchemy] Success: Updated journals table for ID {journal_id}")
        else:
            print(f"--- [SQLAlchemy] Warning: ID {journal_id} not found in journals table.")
            
    except Exception as e:
        print(f"--- [SQLAlchemy ERROR] {str(e)}")
        db.rollback()
    finally:
        db.close()