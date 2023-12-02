import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import datetime
import json

df = pd.read_csv('data.csv')

df['SNO'] = df['SNO'].astype(str)
df = pd.get_dummies(df, columns=['SNO'])

X = df.drop(['Date', 'Time', 'sbi'], axis=1)
y = df['sbi']

# see training data
X.to_csv('see_train.csv', mode='a', index=False, header=False)

# train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
model = RandomForestRegressor(n_estimators=30)
model.fit(X_train, y_train)

print("Model trained.")

prediction_dates = [datetime.datetime(2023, 10, 21) + datetime.timedelta(days=i) for i in range(4)] + \
                   [datetime.datetime(2023, 12, 4) + datetime.timedelta(days=i) for i in range(7)]

with open('/Users/xujinwei/Desktop/ML/html.2023.final.data/sno_test_set.txt') as file:
    sno_test = [line.strip() for line in file]

with open("/Users/xujinwei/Desktop/ML/html.2023.final.data/demographic.json", 'r') as f:
    demographic_data = json.load(f)

prediction_data = []
for prediction_date in prediction_dates:
    for sno in sno_test:
        for hour in range(24):
            for minute in range(0, 60, 20):
                total_minutes = hour * 60 + minute
                sin_time = np.sin(2 * np.pi * total_minutes / 1440)
                cos_time = np.cos(2 * np.pi * total_minutes / 1440)

                id_str = f"{prediction_date.strftime('%Y%m%d')}_{sno}_{hour:02d}:{minute:02d}"
                row = {
                    'id': id_str,
                    'sin_time': sin_time,
                    'cos_time': cos_time, 
                    'dayofweek': prediction_date.weekday(),
                    'lat': demographic_data[sno]['lat'], 
                    'lng': demographic_data[sno]['lng'],
                    f'SNO_{sno}': 1
                }
                for sno_col in df.columns[df.columns.str.startswith('SNO_')]:
                    if sno_col != f'SNO_{sno}':
                        row[sno_col] = 0

                prediction_data.append(row)

prediction_df = pd.DataFrame(prediction_data)

prediction_features = prediction_df.drop('id', axis=1)
predicted_sbi = model.predict(prediction_features)

predicted_sbi_rounded = [round(value) for value in predicted_sbi]
prediction_df['sbi'] = predicted_sbi_rounded
final_predictions = prediction_df[['id', 'sbi']]
final_predictions.to_csv('final_predictions.csv', index=False)
