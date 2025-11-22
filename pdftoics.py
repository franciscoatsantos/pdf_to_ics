import argparse
from parser import Parser
from ics import Calendar, Event


def pdf_to_ics(input_file, output_file):

    parser = Parser(input_file)
    events = parser.parse()

    cal = Calendar()
    unique_events = []
    for event in events:
        if event not in unique_events:
            unique_events.append(event)

    for event_data in unique_events:
        event = Event()
        event.name = event_data["title"]
        event.begin = event_data["start_datetime"]
        event.end = event_data["end_datetime"]
        event.description = event_data["description"]
        cal.events.add(event)

    with open('calendar.ics', 'w') as f:
        f.write(cal.serialize())

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Script to parse pdf files from the IEFP organization so we can extract a calendar file from the pdf")
    
    parser.add_argument("-i", "--input", required=True, help="Path to the PDF file")
    parser.add_argument("-o", "--output", required=False, help="Path to the output .ics file")

    # Parse arguments
    args = parser.parse_args()

    # Get the XML file path from the arguments
    input_file = args.input.strip()

    # Default to nmap_report.md if no args are given for the ouput path
    output_file = "calendar.ics" if not args.output else args.output.strip()

    # Parse the XML and generate the Markdown report
    calendar_file = pdf_to_ics(input_file, output_file)

    # Save the report to a file

    print(f"Calendar generated in: {output_file}")