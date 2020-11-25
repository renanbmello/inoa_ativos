from threading import Thread
from ativos.models import Ativo
from datetime import date, timedelta
from .serializers import AtivoSerializer
import yfinance as yf


class GetAtivo(Thread):

    def __init__(self, symbol, errors):
        Thread.__init__(self)
        self.symbol = symbol
        self.errors = errors

    def run(self):
        query = None
        try:
            query = Ativo.objects.get(symbol=self.symbol["name"])
            exists = query

        except Exception as erro:
            if "matching query does not exist." not in getattr(erro, 'message', str(erro)):
                self.errors.append(getattr(erro, 'message', str(erro)))

        if self.errors:
            return

        ativo = yf.Ticker(self.symbol["name"])
        today = date.today()
        today.strftime("%Y-%m-%d")
        stocks = {
            "oneDay": ativo.history(period="1d", interval="2m").to_json(),
            "fiveDays": ativo.history(period="5d", interval="15m").to_json(),
            "oneMonth": ativo.history(start=(today - timedelta(days=30)).strftime("%Y-%m-%d"), end=today.strftime("%Y-%m-%d")).to_json(),
            "sixMonths": ativo.history(start=(today - timedelta(days=180)).strftime("%Y-%m-%d"), end=today.strftime("%Y-%m-%d")).to_json(),
        }

        body = {
            "longName": ativo.info["longName"],
            "symbol": ativo.info["symbol"],
            "sector": ativo.info["sector"],
            "profitMargins": str(ativo.info["profitMargins"]),
            "stocks": stocks
        }

        if(query != None):  # verificação se é vazio
            serializer = AtivoSerializer(instance=query, data=body)
            if serializer.is_valid():  # valida se o JSON pode ser serializado como ativo
                serializer.save(update_fields=['updated_at'])
            else:
                self.erros.append(serializer.errors)
        else:
            serializer = AtivoSerializer(data=body)
            if serializer.is_valid():  # valida se o JSON pode ser serializado como ativo
                serializer.save()
            else:
                self.erros.append(serializer.errors)
