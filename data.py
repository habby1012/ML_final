import json
import pandas as pd
import os
import random
import numpy as np
from datetime import datetime, timedelta

# get all stations
with open('/Users/xujinwei/Desktop/ML/html.2023.final.data/demographic.json', 'r') as f:
    demographic_data = json.load(f)
all_stations = set(demographic_data.keys())

# get test stations
with open('/Users/xujinwei/Desktop/ML/html.2023.final.data/sno_test_set.txt') as file:
    sno_test = set([line.strip() for line in file])

# randomly choose stations except those test stations
available_stations = all_stations - sno_test
random_stations = random.sample(list(available_stations), 300)

# stations taken to train model
# selected_stations = list(sno_test)
# selected_stations = list(sno_test) + random_stations
selected_stations = list(all_stations)

All_date = os.listdir("/Users/xujinwei/Desktop/ML/html.2023.final.data/release/")

output_file = "data.csv"
df = pd.DataFrame(columns=['SNO', 'Date', 'Time', 'sin_time', 'cos_time', 'dayofweek', 'lat', 'lng', 'sbi'])
df.to_csv(output_file, mode='w', index=False)

with open("/Users/xujinwei/Desktop/ML/html.2023.final.data/demographic.json", 'r') as f:
    demographic_data = json.load(f)

miss = 0
for date in All_date:
    for sno in selected_stations:
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
                        if miss != 0:
                            for i in range(0, miss+1):
                                sbi = values['sbi']

                                time_obj = datetime.strptime(time, "%H:%M")
                                time_obj -= timedelta(seconds=i)
                                formatted_time = time_obj.strftime("%H:%M")

                                hours = time_obj.hour
                                minutes = time_obj.minute
                                total_minutes = hours * 60 + minutes
                                sin_time = np.sin(2 * np.pi * total_minutes / 1440)
                                cos_time = np.cos(2 * np.pi * total_minutes / 1440)

                                date_str = str(date)
                                datetime_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]} {time}"
                                datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                                day_of_week = datetime_obj.weekday()
                                
                                new_rows.append({'SNO': sno, 'Date': date, 'Time': formatted_time, 'sin_time': sin_time, 'cos_time': cos_time, 'dayofweek': day_of_week, 'lat': lat, 'lng': lng, 'sbi': sbi})

                            miss = 0

                        else:
                            sbi = values['sbi']
                            
                            time_obj = datetime.strptime(time, "%H:%M")
                            hours = time_obj.hour
                            minutes = time_obj.minute
                            total_minutes = hours * 60 + minutes
                            sin_time = np.sin(2 * np.pi * total_minutes / 1440)
                            cos_time = np.cos(2 * np.pi * total_minutes / 1440)

                            date_str = str(date)
                            datetime_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]} {time}"
                            datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                            day_of_week = datetime_obj.weekday()

                            new_rows.append({'SNO': sno, 'Date': date, 'Time': time, 'sin_time': sin_time, 'cos_time': cos_time, 'dayofweek': day_of_week, 'lat': lat, 'lng': lng, 'sbi': sbi})

                    else:
                        miss += 1

                new_df = pd.DataFrame(new_rows)
                new_df.to_csv(output_file, mode='a', index=False, header=False)