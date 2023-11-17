import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import datetime
import json

df = pd.read_csv('data.csv')

df['SNO'] = df['SNO'].astype(str)
df = pd.get_dummies(df, columns=['SNO'])

X = df.drop(['Date', 'Time', 'sbi'], axis=1)
y = df['sbi']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

model = RandomForestRegressor(n_estimators=30)
model.fit(X_train, y_train)

prediction_dates = [datetime.datetime(2023, 10, 21) + datetime.timedelta(days=i) for i in range(4)] + \
                   [datetime.datetime(2023, 12, 4) + datetime.timedelta(days=i) for i in range(7)]

with open("/Users/xujinwei/Desktop/ML/html.2023.final.data/demographic.json", 'r') as f:
    demographic_data = json.load(f)

sno_columns = [col for col in df.columns if col.startswith('SNO_')]
prediction_data = []

for prediction_date in prediction_dates:
    for sno_col in sno_columns:
        sno = sno_col.split('_')[1]
        
        for hour in range(24):
            for minute in range(0, 60, 20):
                total_minutes = hour * 60 + minute
                id_str = f"{prediction_date.strftime('%Y%m%d')}_{sno}_{hour:02d}:{minute:02d}"
                row = {
                    'id': id_str,
                    'totalminutes': total_minutes, 
                    'dayofweek': prediction_date.weekday(),
                    'lat': demographic_data[sno]['lat'], 
                    'lng': demographic_data[sno]['lng'] 
                }
                for sno_inner in sno_columns:
                    row[sno_inner] = 1 if sno_inner == sno_col else 0
                prediction_data.append(row)

prediction_df = pd.DataFrame(prediction_data)

prediction_features = prediction_df.drop('id', axis=1)

predicted_sbi = model.predict(prediction_features)

predicted_sbi_rounded = [round(value) for value in predicted_sbi]

prediction_df['sbi'] = predicted_sbi_rounded

final_predictions = prediction_df[['id', 'sbi']]

final_predictions.to_csv('final_predictions.csv', index=False)