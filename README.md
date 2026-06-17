# AI Appointment Booking Assistant

## Overview

#### An automated appointment booking system built using Flask, Google Gemini, Make.com, Tally Forms, ngrok, Google Calendar and Google Sheets.

#### The system receives appointment requests through a Tally form, sends the request to a Flask API for processing, uses Google Gemini to extract the appointment date, time and purpose from natural language, returns the structured information to Make.com, checks Google Calendar for slot availability, automatically books available appointments, stores all records in Google Sheets, and generates professional email drafts for unavailable appointment requests.

## Screenshots

### Tally Form

![TALLY SCR.png](assets/TALLY%20SCR.png)

### Make.com Workflow

![MAKE.COM SCR.png](assets/MAKE.COM%20SCR.png)
### Google Sheets Output (Booked Appointments)

![BOOKED SCR.png](assets/BOOKED%20SCR.png)

### Google Sheets Output (Unavailable Slots)

![NOT BOOKED SCR.png](assets/NOT%20BOOKED%20SCR.png)

### Calendar (With Booked Slots)

![CALENDAR SCR.png](assets/CALENDAR%20SCR.png)

## Features

* Appointment request intake through Tally Forms
* Flask REST API
* Google Gemini 2.5 Flash integration
* Natural language date and time extraction
* Appointment purpose extraction
* Google Calendar availability checking
* Automatic appointment booking
* Professional unavailable-slot email generation
* Make.com automation
* Google Sheets integration
* Customer information management
* Automated workflow routing

## Tech Stack

* Python
* Flask
* Google Gemini 2.5 Flash
* Make.com
* Tally Forms
* Google Calendar
* Google Sheets
* ngrok

## Workflow

Tally Form
↓
Make.com Trigger
↓
HTTP Request
↓
Flask API
↓
Google Gemini Processing
↓
Date / Time / Reason Extraction
↓
Google Calendar Availability Check (Make.com)
↓
Available / Unavailable Router
↓
Create Calendar Event OR Generate Email Draft
↓
Google Sheets

## Sample Input

```json
{
    "name": "Ram Puri",
    "email": "ram@gmail.com",
    "message": "I need a website consultation next Monday at 11 AM"
}
```

## Sample Output (Appointment Booked)

```json
{
    "status": "Confirmed",
    "message": "Appointment booked",
    "name": "Ram Puri",
    "email": "ram@gmail.com",
    "date": "2026-06-22",
    "time": "11:00",
    "reason": "website consultation"
}
```

## Sample Output (Unavailable Slot Email Draft)

```json
{
    "status": "Not Confirmed",
    "email_draft": "Dear Ram Puri, Thank you for your interest in scheduling a website consultation with us. Unfortunately, the requested appointment slot on June 22, 2026 at 11:00 AM is no longer available. We would be happy to arrange another suitable time for you. Please let us know your preferred alternative date and time and we will do our best to accommodate your request. We look forward to hearing from you."
}
```

## Project Structure

```text
ai-appointment-booking-assistant/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
└── assets/
    ├── TALLY SCR.png
    ├── MAKE.COM SCR.png
    ├── BOOKED SCR.png
    └── NOT BOOKED SCR.png
```
