import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# 🔗 Railway PostgreSQL URL
DATABASE_URL = os.environ["DATABASE_URL"]

# Engine
engine = create_engine(DATABASE_URL, echo=False)

# Base model
Base = declarative_base()

# Session
SessionLocal = sessionmaker(bind=engine)


# 📦 EVENTS TABLE
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)

    source = Column(Text)
    company = Column(Text)
    actors = Column(Text)

    event_date = Column(Text)
    location = Column(Text)

    ticket_sale = Column(Text)
    summary = Column(Text)

    url = Column(Text)
    embedding = Column(Text)


# 🔧 CREATE TABLES
def create_table():
    Base.metadata.create_all(bind=engine)


# 💾 SAVE EVENT
def save_event(data):
    session = SessionLocal()

    actors = data.get("actors", [])
    if isinstance(actors, list):
        actors = ", ".join(actors)

    event = Event(
        source=data.get("source", ""),
        company=data.get("company", ""),
        actors=actors,
        event_date=data.get("date", ""),
        location=data.get("location", ""),
        ticket_sale=str(data.get("ticket_sale", False)),
        summary=data.get("summary", ""),
        url=data.get("url", ""),
        embedding=data.get("embedding", "")
    )

    session.add(event)
    session.commit()
    session.close()


# 📊 GET ALL EVENTS
def get_events():
    session = SessionLocal()
    events = session.query(Event).order_by(Event.event_date.asc()).all()
    session.close()
    return events


# 🔍 GET SINGLE EVENT
def get_event(event_id):
    session = SessionLocal()
    event = session.query(Event).filter(Event.id == event_id).first()
    session.close()
    return event


# 🔎 SEARCH EVENTS
def search_events(query):
    session = SessionLocal()

    results = session.query(Event).filter(
        Event.actors.like(f"%{query}%") |
        Event.summary.like(f"%{query}%") |
        Event.location.like(f"%{query}%")
    ).order_by(Event.event_date.asc()).all()

    session.close()
    return results


# ⏳ UPCOMING EVENTS
def get_upcoming_events():
    session = SessionLocal()

    events = session.query(Event)\
        .filter(Event.event_date >= "2026-01-01")\
        .order_by(Event.event_date.asc())\
        .all()

    session.close()
    return events