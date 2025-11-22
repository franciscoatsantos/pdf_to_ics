# pdf_to_google_calendar (ICS exporter)

Extracts events from a structured PDF (e.g., training schedules, timetables) and writes them to an iCalendar (.ics) file.

## Features
- Parses tabular or line‑based date/time blocks from PDF.
- Normalizes titles, dates, start/end times, optional location/instructor.
- Exports a valid .ics file (VEVENT entries).

## Requirements
- Python 3.10+
- A reasonably structured PDF (consistent columns / delimiters).

## Installation
```bash
git clone https://github.com/franciscoatsantos/pdf_to_google_calendar.git
cd pdf_to_google_calendar
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage
```bash
python main.py -i schedule.pdf --out schedule.ics
```
- Then just import the output.ics file into your favourite calendar app(e.g: Google Calendar, Outlook, etc)


## Contributing
Open an issue describing improvements or edge cases. Provide a redacted sample PDF if possible.

## License
MIT.

## Acknowledgments
Uses open-source PDF parsing and iCalendar libraries.
