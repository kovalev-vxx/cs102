import gensim #type: ignore
import pyLDAvis.gensim #type: ignore
from gensim.corpora import Dictionary #type: ignore
from textacy import preprocessing #type: ignore
from tqdm import tqdm #type: ignore
import pymorphy2 #type: ignore

from vkapi.wall import get_wall_execute #type: ignore


def get_topic_model(domain: str = "", count: int = 5000, max_count: int = 1000, progress=tqdm):
    posts = get_wall_execute(domain=domain, count=count, max_count=max_count, progress=progress)
    stopwords = list(map(str.strip, open("stop_words.txt", "r")))
    text_no_urls = map(preprocessing.replace.replace_urls, posts.text.dropna().to_list())
    text_no_punct = map(preprocessing.remove_punctuation, text_no_urls)
    text_no_emojis = map(preprocessing.replace.replace_emojis, text_no_punct)
    text_no_white_space = map(preprocessing.normalize.normalize_whitespace, text_no_emojis)
    docs = map(str.split, text_no_white_space)
    docs = [[word.lower() for word in doc if word not in stopwords] for doc in docs] #type: ignore
    docs = [[word for word in doc if len(word) > 3] for doc in docs] #type: ignore
    docs = [[word for word in doc if word not in stopwords] for doc in docs] #type: ignore
    docs = [[word for word in doc if word not in stopwords] for doc in docs] #type: ignore
    trantab = str.maketrans("0123456789", "          ")
    docs = [[word.translate(trantab) for word in doc] for doc in docs] #type: ignore
    docs = [[word.replace(" ", "") for word in doc if word] for doc in docs] #type: ignore
    docs = [[word for word in doc if word] for doc in docs] #type: ignore
    morph = pymorphy2.MorphAnalyzer()
    docs = [[(morph.parse(word)[0].normal_form) for word in doc] for doc in docs] #type: ignore
    docs = [[word for word in doc if morph.tag(word)[0].POS == "NOUN" or "ADJF"] for doc in docs] #type: ignore
    dictionary = Dictionary(docs)
    corpus = list(dictionary.doc2bow(text) for text in docs)
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=20, id2word=dictionary, passes=15)
    vis = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)
    pyLDAvis.show(vis)


if __name__ == "__main__":
    get_topic_model(domain="rbc")
