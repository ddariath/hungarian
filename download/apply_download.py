import pandas as pd
from download import save_pdf
import requests
from requests.exceptions import Timeout, RequestException

data = pd.read_csv('filtered_hu_data.csv')

sample = data[8800:].copy()
sample['format'] = 'Not defined'

for index, row in sample.iterrows():
    short_url = row['url']
    try:
        save_pdf(short_url, sample)
    except Exception as e:
        print(f'Ошибка загрузки: {e}')

sample.to_csv('sample_8800_end.csv', index=False)




