from icalendar import Calendar, Event
import datetime
from fillpdf import fillpdfs

path=input("Enter ics file path: ")

# first_name="Arya"
# last_name="Salwan"
first_name=input("first_name: ")
last_name=input("last_name: ")
name=first_name +" "+ last_name
template_pdf="/Users/arya/Downloads/PAL leader Time Sheet.pdf"
fields_dict=fillpdfs.get_form_fields(template_pdf)
print(fields_dict)
fields_dict['STUDENT NAME PLEASE PRINT']=name

with open(r'/Users/arya/Downloads/Work2.ics','rb') as file:
    gcal=Calendar.from_ical(file.read())

today = datetime.date.today()
days_since_monday = (today.weekday() - 0) % 7

# Subtract the necessary days to get last Monday
last_monday = today - datetime.timedelta(days=days_since_monday)
friday=last_monday+datetime.timedelta(days=5)
total_hours_worked=datetime.timedelta(hours=0,minutes=0)
list_pal=[]
print(last_monday)
k=1
for component in gcal.walk():
    if component.name == "VEVENT":
        event_start_date = component.get('dtstart').dt
        if type(event_start_date)==datetime.datetime:
            event_start_date=event_start_date.date()
        #print(type(event_start_date))
        #event_start_date = event_start_date.date()
        #event_start_date=event_start_date.date()
        #print(event_start_date)

        if component.name == "VEVENT" and friday>event_start_date>last_monday and ('PAL' in component.get('summary')):
            dstart=component.get('dtstart').dt
            dtend=component.get('dtend').dt
            summary=component.get('summary')
            description=component.get('description','')
            # print('Summary:', summary)
            # print('Start Date:', dstart)
            # print('End Date:', dtend)
            # print('Description:', )
            # print()

            fields_dict[f'DATES WORKEDRow{k}']=event_start_date
            if dstart.minute==0:
                fields_dict[f'Start TimeRow{k}'] = f"{dstart.hour}:{dstart.minute}0"
                fields_dict[f'End TimeRow{k}'] = f"{dtend.hour}:{dtend.minute}0"
            else:
                fields_dict[f'Start TimeRow{k}'] = f"{dstart.hour}:{dstart.minute}"
                fields_dict[f'End TimeRow{k}'] = f"{dtend.hour}:{dtend.minute}"

            duration=(dtend - dstart)
            total_hours_worked += duration
            duration=str(duration)
            duration=duration[:-3]
            fields_dict[f"DAILY HOURSRow{k}"]=duration
            fields_dict[f"DESCRIPTION OF WORKRow{k}"]=description
            k+=1

fields_dict['TOTAL HOURS WORKED']=str(total_hours_worked)[:-3]
fields_dict['Date']=str(today)
text=f"Attached is my student time sheet outlining hours worked from {last_monday}. I can confirm that the hours outlined on the attached are correct and were worked as indicated."
print(text)
fillpdfs.write_fillable_pdf(template_pdf, f"{last_name},{first_name} for week ending {friday}test.pdf", fields_dict)