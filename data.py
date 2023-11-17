import json
import pandas as pd
import json
import os
from datetime import datetime


with open('/Users/xujinwei/Desktop/ML/html.2023.final.data/sno_test_set.txt') as file:
    sno_test = [line.strip() for line in file]

All_date = os.listdir("/Users/xujinwei/Desktop/ML/html.2023.final.data/release/")

df = pd.DataFrame(columns=['SNO', 'Date', 'Time', 'totalminutes', 'dayofweek', 'lat', 'lng', 'sbi'])

with open("/Users/xujinwei/Desktop/ML/html.2023.final.data/demographic.json", 'r') as f:
    demographic_data = json.load(f)

for date in All_date:
    for sno in sno_test:
        item = demographic_data.get(str(sno), {})
        lat = item.get("lat")
        lng = item.get("lng")

        json_file = "/Users/xujinwei/Desktop/ML/html.2023.final.data/release/" + date + "/" + sno + ".json"

        if os.path.exists(json_file):
            with open(json_file, 'r') as file:
                data = json.load(file)

                new_rows = []
                for time, values in data.items():
                    if 'sbi' in values:
                        sbi = values['sbi']
                        
                        time_obj = datetime.strptime(time, "%H:%M")
                        hours = time_obj.hour
                        minutes = time_obj.minute
                        total_minutes = hours * 60 + minutes

                        date_str = str(date)
                        datetime_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]} {time}"
                        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                        day_of_week = datetime_obj.weekday()

                        new_rows.append({'SNO': sno, 'Date': date, 'Time': time, 'totalminutes': total_minutes, 'dayofweek': day_of_week, 'lat': lat, 'lng': lng, 'sbi': sbi})

                new_df = pd.DataFrame(new_rows)
                df = pd.concat([df, new_df], ignore_index=True)

output_file_path = 'data.csv'
df.to_csv(output_file_path, index=False)