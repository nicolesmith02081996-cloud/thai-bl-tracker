import os
from flask import Flask, render_template, request

from database import (
    create_table,
    get_events,
    get_event,
    search_events,
    get_upcoming_events
)

app = Flask(__name__)

# 🔧 ensure DB is created on startup
create_table()


# 🏠 HOME PAGE
@app.route("/")
def home():

    query = request.args.get("query")

    if query:
        events = search_events(query)
    else:
        events = get_events()

    return render_template(
        "home.html",
        events=events,
        event_count=len(events),
        query=query
    )


# 📅 CALENDAR PAGE
@app.route("/calendar")
def calendar():

    events = get_events()

    return render_template(
        "calendar.html",
        events=events
    )


# 📌 SINGLE EVENT PAGE
@app.route("/event/<int:event_id>")
def event(event_id):

    event = get_event(event_id)

    if not event:
        return "Event not found", 404

    return render_template(
        "event.html",
        event=event
    )


# 🔍 UPCOMING EVENTS PAGE (optional but useful)
@app.route("/upcoming")
def upcoming():

    events = get_upcoming_events()

    return render_template(
        "home.html",
        events=events,
        event_count=len(events),
        query="upcoming"
    )


# 🚀 RUN (Railway safe)
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )