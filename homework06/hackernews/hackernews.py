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
def change_label():
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
    s = get_session(engine)
    model = NaiveBayesClassifier(alpha=0.05)
    labeled_news = s.query(News).filter(News.label != None).all()
    if len(labeled_news) == 0:
        redirect(".")
    unlabeled_news = s.query(News).filter(News.label == None).all()

    X, y = [], []
    for news in labeled_news:
        X.append(news.title)
        y.append(news.label)

    model.fit(X, y)

    pr_news = model.predict([news.title for news in unlabeled_news])
    liked_news = []
    maybe_news = []

    for cl,news in zip(pr_news["pred_class"], unlabeled_news):
        if cl == "like":
            liked_news.append(news)
        elif cl == "maybe":
            maybe_news.append(news)


    return template('templates/recommendations.tpl', liked_news=liked_news, maybe_news = maybe_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)

    