from icalendar import Calendar, Event

def remove_event_by_summary(calendar, summary_to_remove):
    # Use a list comprehension to filter out the event
    calendar.subcomponents = [
        event for event in calendar.subcomponents if event.name == "VEVENT" and event.get('summary') != summary_to_remove
    ]

# Assuming gcal is already loaded from your file:
file_path = '/Users/arya/Downloads/Work2.ics'
summary_to_remove = "PAL: Barry Power CHEM1050"

# Load the calendar
with open(file_path, 'rb') as file:
    gcal = Calendar.from_ical(file.read())

# Call the function to remove the event
remove_event_by_summary(gcal, summary_to_remove)

# Save the modified calendar back to the file
with open(file_path, 'wb') as file:
    file.write(gcal.to_ical())
