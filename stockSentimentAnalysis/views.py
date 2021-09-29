from django.shortcuts import render, HttpResponse
import json
import string
import joblib
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import tensorflow as tf
from newsapi import NewsApiClient
import requests    


ps = PorterStemmer()
stopWords = stopwords.words("english")

_model = None
_vectorizer = None


def load_artifacts():
    global _model
    global _vectorizer

    _model = tf.keras.models.load_model(
        "./stockSentimentAnalysis/artifacts/model")
    _vectorizer = joblib.load(
        "./stockSentimentAnalysis/artifacts/vectorizer.pkl")


def fun(x):
    x = x.lower()
    x = re.sub(r"[^a-zA-Z]", " ", x)
    x = x.split()
    x = [ps.stem(i) for i in x if i not in stopWords]
    x = " ".join(x)
    x = [x]
    print(x)
    x = _vectorizer.transform(x).toarray()
    return x


def home(request):
    context = {
        "title": "ML-TOOLBOX"
    }
    return render(request, 'stockSentimentAnalysis/home.html', context)


def predictStocks(request):
    if request.method == "POST":
        load_artifacts()
        headline = request.POST.get("headline")
        headline = fun(headline)
        result = int(_model.predict(headline)[0][0] > 0.3)
        return HttpResponse(json.dumps({"res": result}))
    else:
        return HttpResponse(json.dumps({"status": "failed"}))


def getHeadlines(request):
    if request.method == "POST":
        query_params = {
            "source": "bbc-news",
            "sortBy": "top",
            "apiKey": "5c0c87aa0c6741e8a0ac48d4ea16210b"
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

if __name__ == "__main__":
    getHeadlines()
