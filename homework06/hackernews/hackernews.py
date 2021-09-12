from bottle import (
    route, run, template, request, redirect
)

from db import News, get_session, engine, update_label, get_fresh_news, clear_without_label_news, clear_labels
from bayes import NaiveBayesClassifier


@route("/")
def news_list():
    return template('templates/main_template.tpl')


@route("/news")
def news_list():
    s = get_session(engine)
    rows = s.query(News).filter(News.label == None).all()
    return template('templates/news_template.tpl', rows=rows)

@route("/clear")
def clear():
    clear_without_label_news(get_session(engine))
    redirect("/news")

@route("/clear_labels")
def clear_all_labels():
    clear_labels(get_session(engine))
    redirect("/labeled_news")


@route("/add_label/")
def add_label():
    s = get_session(engine)
    id = request.query["id"]
    label = request.query["label"]
    update_label(id = id,label = label, session = s)
    redirect("/news")

@route("/change_label/")
def add_label():
    s = get_session(engine)
    id = request.query["id"]
    label = request.query["label"]
    update_label(id = id,label = label, session = s)
    redirect("/labeled_news")


@route("/update")
def update_news():
    get_fresh_news(session=get_session(engine))
    redirect("/news")

@route("/labeled_news")
def labeled_news_list():
    s = get_session(engine)
    liked_news = s.query(News).filter(News.label == "like").all()
    maybe_news = s.query(News).filter(News.label == "maybe").all()
    disliked_news = s.query(News).filter(News.label == "dislike").all()
    return template('templates/labeled_news_template.tpl', liked_news=liked_news, disliked_news=disliked_news, maybe_news = maybe_news)


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080)

    