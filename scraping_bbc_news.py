import requests
from bs4 import BeautifulSoup
from db import db_session
from models import News


def add_news(headline, ful_ref):

    news = News(headline=headline, ful_ref=ful_ref)
    db_session.add(news)
    db_session.commit()
    db_session.close()

def scriping_bbc():

    # specify the URL of the news website you want to scrape
    url = 'https://www.bbc.com/news/world'

    # send a request to the website and get its HTML content
    response = requests.get(url)
    html_content = response.content

    # parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(html_content, 'html.parser')
    # print (soup)

    # find all the news articles on the page
    news_articles = soup.find_all('a', class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor')



    # loop through the news articles and print out their headlines and summaries
    for article in news_articles:
        headline = article.find('h3', class_='gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text').text.strip()
        reference = article.get('href')
        if reference[0] == '/':
            ful_ref = 'https://www.bbc.com'+reference

        check_title = db_session.query(News.headline).filter(News.headline == headline).first()

        if not check_title:

            add_news(headline, ful_ref)


if __name__ == '__main__':
    scriping_bbc()
