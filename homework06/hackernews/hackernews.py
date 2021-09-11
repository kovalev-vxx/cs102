from bottle import (
    route, run, template, request, redirect
)

#from scrapper import get_news 
from db import News, get_session, engine, update_label, get_fresh_news, clear_without_label_news
from bayes import NaiveBayesClassifier


@route("/")
def news_list():
    return template('/Users/kovalev-vxx/Code/cs102/homework06/hackernews/main.tpl')


@route("/news")
def news_list():
    s = get_session(engine)
    rows = s.query(News).filter(News.label == None).all()
    return template('/Users/kovalev-vxx/Code/cs102/homework06/hackernews/news_template.tpl', rows=rows)

@route("/clear")
def clear():
    clear_without_label_news(get_session(engine))
    redirect("/news")


@route("/add_label/")
def add_label():
    s = get_session(engine)
    id = request.query["id"]
    label = request.query["label"]
    update_label(id = id,label = label, session = s)
    redirect("/news")


@route("/update")
def update_news():
    get_fresh_news(session=get_session(engine))
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    pass


if __name__ == "__main__":

    run(host="localhost", port=8080)

