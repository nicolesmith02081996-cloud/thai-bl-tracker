# app.py

from flask import Flask, render_template, request
from datetime import datetime
import os

from database import (
    create_table,
    get_events,
    get_event,
    search_events,
    get_upcoming_events,
    get_stats
)

app = Flask(__name__)

# =========================================================
# DATABASE SETUP
# =========================================================

create_table()


# =========================================================
# HELPERS
# =========================================================

def days_until(date_string):

    """
    Returns number of days until event.
    """

    if not date_string:
        return None

    formats = [

        "%Y-%m-%d",
        "%d %b %Y",
        "%d %B %Y",
        "%m/%d/%Y"

    ]

    for fmt in formats:

        try:

            event_date = datetime.strptime(
                date_string,
                fmt
            )

            today = datetime.now()

            return (event_date - today).days

        except:
            continue

    return None


# Make available in templates
app.jinja_env.globals.update(
    days_until=days_until
)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    query = request.args.get(
        "q",
        ""
    ).strip()

    try:

        if query:
            events = search_events(query)

        else:
            events = get_events()

        stats = get_stats()

        return render_template(

            "home.html",

            events=events,

            query=query,

            total_events=stats.get(
                "total_events",
                0
            ),

            total_companies=stats.get(
                "companies",
                0
            ),

            total_locations=stats.get(
                "locations",
                0
            )
        )

    except Exception as e:

        print("Home page error:", e)

        return render_template(

            "home.html",

            events=[],

            query=query,

            total_events=0,

            total_companies=0,

            total_locations=0
        )


# =========================================================
# EVENT DETAILS PAGE
# =========================================================

@app.route("/event/<int:event_id>")
def event_page(event_id):

    try:

        event = get_event(event_id)

        if not event:

            return render_template(

                "error.html",

                message="Event not found."

            ), 404

        return render_template(

            "event.html",

            event=event
        )

    except Exception as e:

        print("Event page error:", e)

        return render_template(

            "error.html",

            message="Unable to load event."

        ), 500


# =========================================================
# UPCOMING EVENTS PAGE
# =========================================================

@app.route("/upcoming")
def upcoming():

    try:

        events = get_upcoming_events()

        return render_template(

            "upcoming.html",

            events=events
        )

    except Exception as e:

        print("Upcoming page error:", e)

        return render_template(

            "upcoming.html",

            events=[]
        )


# =========================================================
# COMPANY PAGE
# =========================================================

@app.route("/company/<company_name>")
def company_page(company_name):

    try:

        events = search_events(company_name)

        return render_template(

            "home.html",

            events=events,

            query=company_name,

            total_events=len(events),

            total_companies=1,

            total_locations=0
        )

    except Exception as e:

        print("Company page error:", e)

        return render_template(

            "home.html",

            events=[],

            query=company_name,

            total_events=0,

            total_companies=0,

            total_locations=0
        )


# =========================================================
# HEALTH CHECK (RAILWAY)
# =========================================================

@app.route("/health")
def health():

    return {

        "status": "ok",

        "service": "Thailand BL Tracker"

    }


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(404)
def not_found(error):

    return render_template(

        "error.html",

        message="Page not found."

    ), 404


@app.errorhandler(500)
def internal_error(error):

    return render_template(

        "error.html",

        message="Internal server error."

    ), 500


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(

        host="0.0.0.0",

        port=port,

        debug=False
    )