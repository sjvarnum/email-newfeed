import os
import requests

from dotenv import load_dotenv

load_dotenv()


class NewsFeed:
    """Collect articles of interest and email to users. Add users to email_addr.csv
    with their interest.

    CSV Fields:
    email,first_name,last_name,interest

    ex. joe.doe@example.com,John,Doe,bitcoin

    Return: Listing of articles that will be inserted into the email body
    """

    api_key = os.environ.get('api_key')
    url = f'https://newsapi.org/v2/everything?'

    def __init__(self, interest=None, from_date=None, to_date=None, language='en'):
        self.interest = interest
        self.from_date = from_date
        self.to_date = to_date
        self.language = language

    def get(self):
        """Fetch articles from API

        Keyword arguments:
        interest -- keyword to search for in articles
        from_date -- starting date range
        to_date -- ending date range
        language -- preferred language - defaults to English
        Return: list of articles for interest within given date range
        """

        params = {
            'q': f'{self.interest}',
            'from': f'{self.from_date}',
            'to': f'{self.to_date}',
            'language': f'{self.language}',
            'apiKey': f'{self.api_key}'
        }

        url = self.url
        response = requests.get(url, params=params)
        response_json = response.json()
        articles = response_json['articles']

        email_body = ''
        for article in articles:
            source = article['source']['name']
            date = article['publishedAt']
            title = article['title']
            description = article['description']
            content = article['content']
            url = article['url']
            email_body = f'{email_body} Date: {date} \n ' \
                f'Source: {source} \n ' \
                f'Title: {title}\n ' \
                f'Description: {description} \n ' \
                f'Content: {content} \n' \
                f'Link: {url} \n\n'

        return email_body


if __name__ == '__main__':
    news_feed = NewsFeed('pharma', '2022-03-01', '2022-03-05', 'en')
    print(news_feed.get())
