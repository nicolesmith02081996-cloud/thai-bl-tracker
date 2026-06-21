from flask import Flask, render_template, request

from database import (
    get_events,
    get_event,
    search_events,
    get_upcoming_events,
    create_table
)

app = Flask(__name__)

create_table()


@app.route("/")
def home():

    query = request.args.get("q")

    if query:
        events = search_events(query)
    else:
        events = get_events()

    return render_template(
        "home.html",
        events=events,
        query=query
    )


@app.route("/event/<int:event_id>")
def event(event_id):

    event = get_event(event_id)

    return render_template(
        "event.html",
          event=event
    )


@app.route("/upcoming")
def upcoming():

    events = get_upcoming_events()

    return render_template(
        "home.html",
        events=events
    )


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )