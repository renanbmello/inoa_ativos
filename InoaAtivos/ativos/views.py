from django.shortcuts import render
import requests
import json
from .serializers import AtivoSerializer
from ativos.models import Ativo
import yfinance as yf
from datetime import datetime


def home(requests):
    query = Ativo.objects.all()

    serializer = AtivoSerializer(
        query, many=True)

    for ativo in serializer.data:
        ticker = yf.Ticker(ativo["symbol"])
        res = ticker.history(
            period="1d", interval="2m")

        ativo["symbol"] = ativo["symbol"].replace(".SA", "")
        stocks = ativo["stocks"]
        openValues = json.loads(stocks["oneDay"])["Close"]
        lastKey = list(openValues.keys())[-2]
        ativo["open"] = openValues[lastKey]
        st = str(lastKey)[0:-3]
    print(ativo["open"])
    print(datetime.fromtimestamp(int(st)))
    return render(requests, 'home.html', context={"ativos": serializer.data})


def acao(requests):
    return render(requests, 'acao.html')
