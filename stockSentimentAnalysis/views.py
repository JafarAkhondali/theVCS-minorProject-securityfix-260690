from django.shortcuts import render, HttpResponse
import json
import joblib
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import requests
from nltk.tokenize import word_tokenize
import joblib
import json
from minorProject.settings import NEWS_PAPER_API

def load_artifacts():
    model = joblib.load("./stockSentimentAnalysis/artifacts/model.pkl")
    with open("./stockSentimentAnalysis/artifacts/allWords.json") as f:
        all_words = json.load(f)

    return model, all_words["allWords"]


ps = PorterStemmer()
stopWords = stopwords.words("english")


def fun(x):
    x = x.lower()
    x = re.sub(r"[^a-zA-Z]", " ", x)
    x = word_tokenize(x)
    x = [word for word in x if word not in stopWords]
    x = [ps.stem(word) for word in x]

    return x


def getFeatures(allWords, document):
    document = set(document)
    features = {}

    for word in allWords:
        features[word] = (word in document)

    return features


def home(request):
    context = {
        "title": "ML-TOOLBOX"
    }
    return render(request, 'stockSentimentAnalysis/home.html', context)


def predictStocks(request):
    if request.method == "POST":
        _model, all_words = load_artifacts()
        headline = request.POST.get("headline")
        headline = fun(headline)
        feature_set = getFeatures(all_words, headline)
        result = _model.classify(feature_set)
        return HttpResponse(json.dumps({"res": int(result==1)}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def getHeadlines(request):
    if request.method == "POST":
        query_params = {
            "source": "bbc-news",
            "sortBy": "top",
            "apiKey": NEWS_PAPER_API
        }

        main_url = " https://newsapi.org/v1/articles"

        res = requests.get(main_url, params=query_params)
        open_bbc_page = res.json()

        article = open_bbc_page["articles"]

        headlines = []

        for ar in article:
            headlines.append({
                "title": ar["title"],
                "url": ar["url"]
            })

        return HttpResponse(json.dumps({"headlines": headlines}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


# if __name__ == "__main__":
