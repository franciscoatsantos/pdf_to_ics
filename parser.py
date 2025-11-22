import re
import pdfplumber
from datetime import datetime


class Parser:

    MONTH_DICT = {
        'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6,
        'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12
    }

    
    def __init__(self, file):
        self.file = file
        month_keys = '|'.join(self.MONTH_DICT.keys())
        self.month_year_re_pattern = rf'\b(?:{month_keys})/\d{{2}}\b'
        self.time_re_pattern = r'^\d{2}H\d{2}\s/\s\d{2}H\d{2}$'

    def parse(self):
        
        pdf = pdfplumber.open(self.file)
        page = pdf.pages[0]
        table_list = page.extract_tables()
        
        # Removing the first table because the calendar only starts in the second index
        table_list.pop(0)
        table_list.remove(table_list[-1])
        
        # events should look like this
        #   events = [
        #       {
        #           "title" : "Formacao IEFP"
        #           "description" : f" Modulo {module_number}"            
        #           "start_datetime" : datetime
        #           "end_datetime" : datetime
        #       }
        #   ]

        event_calendar = []
        for table in table_list:
            # Removing index 2 because it's empty
            table.pop(2)

            # Getting month and year that are always in the first index of the first list
            month, year = self.get_month_year(table[0][0])

            # Build events in-place (duplicate fix, because I screwed up teh first time)
            self.build_json(tables=table, index=2, month=month, year=year, events=event_calendar)



            
        return event_calendar
    
    def get_month_year(self, value):
        try:
            matches = re.findall(self.month_year_re_pattern, value, flags=re.IGNORECASE)
            
            month = str(self.MONTH_DICT[matches[0].split("/")[0].lower()])
            year = str(datetime.today().year)[:2] + matches[0].split("/")[1]
            if datetime.today().month > int(month) and datetime.today().year == int(year): # There are some typos in the file I was provided
                abbr_year = str(int(matches[0].split("/")[1]) + 1)

            return month, year
        except Exception as e:
            print(f"Error parsing month and year: {e}")


    def build_json(self, tables: list, index: int, month: str, year: str, events: list) -> list:
        if index >= len(tables):
            return events
        matches = re.match(self.time_re_pattern, tables[index][0], flags=re.IGNORECASE)
        if matches:
            start = matches[0].split("/")[0].strip()
            end = matches[0].split("/")[1].strip()
            start_hour = start.split("H")[0].strip()
            start_min = start.split("H")[1].strip()
            end_hour = end.split("H")[0].strip()
            end_min = end.split("H")[1].strip()

        for idx, item in enumerate(tables[index]):
            if item and not re.match(self.time_re_pattern, item, flags=re.IGNORECASE):
                day = tables[1][idx]
                obj = {
                    "title": "Formacao",
                    "start_datetime": datetime(int(year), int(month), int(day), int(start_hour), int(start_min)),
                    "end_datetime": datetime(int(year), int(month), int(day), int(end_hour), int(end_min)),
                    "description" : f"Modulo {item}"

                }
                events.append(obj)
        return self.build_json(tables=tables, index=index+1, month=month, year=year, events=events)
        
