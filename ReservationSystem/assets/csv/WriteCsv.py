import csv
from datetime import datetime, timedelta

start_date = datetime(2023, 5, 1)
end_date = datetime(2023, 9, 30)
jet_skis = ['spark', '130', '170']

def is_valid_start_time(hour):
    earliest_start = 10
    latest_end = 22
    return hour >= earliest_start and hour < latest_end

with open('availability.csv', 'w', newline='') as csvfile:
    fieldnames = ['date', 'time_slot'] + jet_skis
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    current_date = start_date
    while current_date <= end_date:
        for hour in range(24):
            if is_valid_start_time(hour):
                slot_start = current_date + timedelta(hours=hour)
                slot_end = current_date + timedelta(hours=hour + 1)
                row = {
                    'date': current_date.strftime('%Y/%m/%d'),
                    'time_slot': f"{slot_start.strftime('%H:%M')}-{slot_end.strftime('%H:%M')}",
                }
                for jet_ski in jet_skis:
                    row[jet_ski] = ''
                writer.writerow(row)
        current_date += timedelta(days=1)
