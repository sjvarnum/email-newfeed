import os

import pandas as pd
import yagmail

from datetime import datetime, date, timedelta
from dotenv import load_dotenv

from news import NewsFeed

load_dotenv()

user_list = pd.read_csv('email_addr.csv')
user = os.environ.get('sender_username')
pwd = os.environ.get('sender_password')
today = date.today()
yesterday = today - timedelta(days=1)

for index, row in user_list.iterrows():
    news_feed = NewsFeed(interest=row['interest'],
                         from_date=today,
                         to_date=yesterday,
                         language='en')
    email = yagmail.SMTP(user=user, password=pwd)
    email.send(
        to=row['email'],
        subject=f'Daily {row["interest"]} news feed for {today}',
        contents=f'Here is your daily {row["interest"]} news feed for {today} \n\n {news_feed.get()}\n\n'
    )
