import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """Extract news from a given web page"""
    news_list = []
    news = parser.find_all(class_="storylink")
    subtext = parser.find_all(class_="subtext")

    for i in range(len(news)):
        url = news[i]["href"]
        title = news[i].get_text()

        sub_item = subtext[i]

        points = sub_item.find(class_="score")
        if points:
            points = int(points.get_text().split()[0])
        else:
            points = 0

        author = sub_item.find(class_="hnuser")
        if author:
            author = author.get_text()

        comments = sub_item.findAll("a", href=True)[-1].get_text().split()
        if "comments" in comments:
            comments = int(comments[0])
        else:
            comments = 0

        news_list.append(
            {
                "author": author,
                "comments": comments,
                "points": points,
                "title": title,
                "url": url,
            }
        )
    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    link = parser.find(class_="morelink")["href"]
    return str(link)


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
