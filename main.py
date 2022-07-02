from datetime import date, timedelta
import pandas as pd
import warnings
import requests


warnings.filterwarnings("ignore")
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)

today = date.today()
yesterday = today - timedelta(days=1)

# Last 7 day (not include today)
#
# URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/istanbul/last7days?unitGroup=metric&elements=datetime%2Ctempmax%2Ctempmin%2Ctemp&key=Q4XWJL3XM9K5ANQVCASFC9RC9&contentType=json"
# df = pd.read_json(URL)
# result = pd.DataFrame()
#
#
# for i in range(len(df.days)):
#     data = pd.DataFrame.from_dict(df.days[i])
#     data.drop(['hours'], axis=1, inplace=True)
#     data.drop_duplicates(keep='first', inplace=True)
#     result = result.append(data, ignore_index=True)
# result.to_csv('temp/result.csv', index=False)


# Today
result = pd.read_csv('temp/result.csv')

URL_2 = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/istanbul/today?unitGroup=metric&elements=datetime%2Ctempmax%2Ctempmin%2Ctemp&key=Q4XWJL3XM9K5ANQVCASFC9RC9&contentType=json"
json = requests.get(URL_2).json()
df_2 = pd.json_normalize(json)


for i in range(len(df_2.days)):
    data_2 = pd.DataFrame.from_dict(df_2.days[i])
    data_2.drop(['hours'], axis=1, inplace=True)
    data_2.drop_duplicates(keep='first', inplace=True)
    result = result.append(data_2, ignore_index=True)
result['datetime'] = pd.to_datetime(result['datetime'])
result.to_csv('temp/result.csv', index=False)


