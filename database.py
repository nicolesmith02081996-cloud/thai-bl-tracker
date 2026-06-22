import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# -------------------------------------------------
# DATABASE SETUP
# -------------------------------------------------
DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# -------------------------------------------------
# TABLE MODEL
# -------------------------------------------------
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)

    source = Column(Text)
    company = Column(Text)
    actors = Column(Text)

    event_date = Column(Text)
    location = Column(Text)

    ticket_sale = Column(Text)
    summary = Column(Text)

    url = Column(Text)
    embedding = Column(Text)


# -------------------------------------------------
# INIT DB
# -------------------------------------------------
def create_table():
    Base.metadata.create_all(bind=engine)


# -------------------------------------------------
# SAVE EVENT
# -------------------------------------------------
def save_event(data):

    session = SessionLocal()

    try:
        event = Event(
            source=data.get("source", ""),
            company=data.get("company", ""),
            actors=", ".join(data.get("actors", []))
            if isinstance(data.get("actors"), list)
            else data.get("actors", ""),

            event_date=data.get("date", ""),
            location=data.get("location", ""),

            ticket_sale=str(data.get("ticket_sale", False)),
            summary=data.get("summary", ""),

            url=data.get("url", ""),
            embedding=data.get("embedding", "")
        )

        session.add(event)
        session.commit()

    except Exception as e:
        session.rollback()
        print("❌ DB Error:", e)

    finally:
        session.close()


# -------------------------------------------------
# GET EVENTS
# -------------------------------------------------
def get_events():

    session = SessionLocal()
    events = session.query(Event).order_by(Event.event_date.asc()).all()
    session.close()

    return events


# -------------------------------------------------
# GET SINGLE EVENT
# -------------------------------------------------
def get_event(event_id):

    session = SessionLocal()
    event = session.query(Event).filter(Event.id == event_id).first()
    session.close()

    return event


# -------------------------------------------------
# DUPLICATE CHECK (simple embedding match placeholder)
# -------------------------------------------------
def is_duplicate(new_embedding):

    if not new_embedding:
        return False

    session = SessionLocal()

    existing = session.query(Event.embedding).filter(Event.embedding.isnot(None)).all()

    session.close()

    for (emb,) in existing:
        if emb and emb == new_embedding:
            return True

    return False