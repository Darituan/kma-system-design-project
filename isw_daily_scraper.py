import os
import urllib.request
from datetime import datetime, timedelta
import time
import pytz
import requests

REPORTS_FOLDER = 'isw_reports'
COLLECT_TIME = '23:30'

def collect_reports():
    eastern_tz = pytz.timezone('US/Eastern')
    now = datetime.now(eastern_tz)
    #if now.strftime('%H:%M') != COLLECT_TIME:
    #    return
    
    today = datetime.now().date()
    file_name = today.strftime('%B_%d_%Y') + '.html'
    file_path = os.path.join(REPORTS_FOLDER, file_name)
    if os.path.exists(file_path):
        print(f'{file_name} already exists.')
        return
    url_date_str = today.strftime('%B-%d-%Y').lower()
    url = f'https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-{url_date_str}'
    response = requests.get(url)
    if response.status_code == 200:
      with open(file_path, 'wb') as f:
        f.write(response.content)
        print(f'{file_name} saved.')
    else:
        print(f'Failed to download {file_name}. Status code: {response.status_code}')

while True:
    collect_reports()
    time.sleep(60)
