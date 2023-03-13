import os
import requests
from datetime import datetime, timedelta
 
if not os.path.exists('isw_reports'):
    os.mkdir('isw_reports')
 
start_date = datetime(2022, 2, 24)
end_date = datetime(2023, 1, 25)
 
date = start_date
while date <= end_date: 
    if date == datetime(2022, 2, 24):
        url = 'https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-initial-russian-offensive-campaign-assessment'
    elif date == datetime(2022, 2, 25):
        url = 'https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-25-2022'
    elif   datetime(2022, 2, 26)<=date<=datetime(2022, 2, 27):
        url = 'https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-26'
    elif date == datetime(2022, 2, 28):
        url = 'https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-28-2022'
    elif date == datetime(2022, 5, 5):
        url = 'https://www.understandingwar.org/backgrounder/russian-campaign-assessment-may-5'
    elif date == datetime(2022, 7, 11):
        url = 'https://understandingwar.org/backgrounder/russian-offensive-campaign-update-july-11'
    elif date == datetime(2022, 8, 12):
        url = 'https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-august-12-0'
    elif date.year == 2022:
        url_date_str = date.strftime('%B-%d').lower().replace('0', '')
        url = f'https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-{url_date_str}'
    elif datetime(2023, 1, 2) <= date <= datetime(2023, 1, 9):
        url_date_str = date.strftime('%d').lower().replace('0', '')
        url = f'https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-january-{url_date_str}-2023'
    else:
        url_date_str = date.strftime('%B-%d-%Y').lower()
        url = f'https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-{url_date_str}'
 
    response = requests.get(url)
 
    if len(response.content) > 15000:
        filename = date.strftime('%B_%d_%Y') + '.html'
        filepath = os.path.join('isw_reports', filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Warning: File for {url} is too small and was not saved.")
 
    date += timedelta(days=1)
