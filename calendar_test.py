from icalendar import Calendar
import requests
from datetime import datetime, timezone

# URL of the Canvas .ics file
ics_url = "https://howardcc.instructure.com/feeds/calendars/user_3a1R4w3Vd0DuP7TNtNreCSFO8CZUUJg9Jrfn844P.ics"

def fetch_and_parse_ics(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        calendar = Calendar.from_ical(response.content)

        # Lists to categorize events
        overdue_events = []
        upcoming_events = []
        completed_events = []

        # Current time to compare with event dates
        current_time = datetime.now(timezone.utc)

        for component in calendar.walk():
            if component.name == "VEVENT":
                summary = component.get("summary")
                start_date = component.get("dtstart").dt
                status = component.get("status", "").lower()  # Check if the event has a status

                # Determine if event is overdue, upcoming, or completed
                if "completed" in summary.lower() or status == "completed":
                    completed_events.append(f"<li class='completed-item'><s>{summary}</s><span class='date'>{start_date.strftime('%A, %B %d, %Y %I:%M %p')}</span></li>")
                elif start_date < current_time:
                    overdue_events.append(f"<li class='overdue-item'><strong>{summary} (Overdue)</strong><span class='date'>{start_date.strftime('%A, %B %d, %Y %I:%M %p')}</span></li>")
                else:
                    upcoming_events.append(f"<li class='upcoming-item'><strong>{summary}</strong><span class='date'>{start_date.strftime('%A, %B %d, %Y %I:%M %p')}</span></li>")

                print(f"Processed event: {summary} - Start Date: {start_date}")  # Debug print statement

        return overdue_events, upcoming_events, completed_events

    except Exception as e:
        print(f"Error fetching or parsing .ics file: {e}")
        return [], [], []

# Fetch and categorize events
overdue_events, upcoming_events, completed_events = fetch_and_parse_ics(ics_url)

# Write the HTML file with categorized lists
with open("index.html", "w") as file:
    file.write("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Canvas Calendar To-Do List</title>
      <link href="https://fonts.googleapis.com/css2?family=Open+Sans&display=swap" rel="stylesheet">
      <style>
        body { font-family: 'Open Sans', sans-serif; background-color: #f4f4f9; color: #333; max-width: 500px; margin: 20px auto; padding: 20px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #3a3a3a; font-size: 1.8em; }
        ul { list-style-type: none; padding: 0; }
        .overdue-item { color: #e74c3c; font-weight: bold; }
        .upcoming-item { color: #2c3e50; }
        .completed-item { color: #95a5a6; text-decoration: line-through; }
        .date { display: block; font-size: 0.9em; color: #6c757d; }
      </style>
    </head>
    <body>
      <h1>Canvas To-Do List</h1>
      <h2>Overdue Assignments</h2>
      <ul>
    """)
    if overdue_events:
        file.write("\n".join(overdue_events))
    else:
        file.write("<li>No overdue assignments.</li>")
    
    file.write("""
      </ul>
      <h2>Upcoming Assignments</h2>
      <ul>
    """)
    if upcoming_events:
        file.write("\n".join(upcoming_events))
    else:
        file.write("<li>No upcoming assignments.</li>")
    
    file.write("""
      </ul>
      <h2>Completed Assignments</h2>
      <ul>
    """)
    if completed_events:
        file.write("\n".join(completed_events))
    else:
        file.write("<li>No completed assignments.</li>")
    
    file.write("""
      </ul>
    </body>
    </html>
    """)
    
print("HTML file 'index.html' generated successfully.")
