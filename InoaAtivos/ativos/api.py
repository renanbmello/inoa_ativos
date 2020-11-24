from ativos.models import Ativo
from rest_framework import viewsets, permissions, status
import requests
from .serializers import AtivoSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import json
import yfinance as yf
from datetime import date, timedelta


class AtivoViewSet (viewsets.ModelViewSet):
    @action(detail=False, methods=['get'])  # escolhendo o metodo
    def get_ativo_data(self, request):
        exists = None
        erros = []
        permissions_classes = [
            permissions.AllowAny
        ]
        query = None

        try:
            query = Ativo.objects.get(symbol="BPAC11.SA")
            exists = query

        except Exception as erro:
            erros.append(erro)
            return Response(str(erro))

        ativo = yf.Ticker("BPAC11.SA")
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
        # serializer = AtivoSerializer(query, data=body)

        if(exists != None):  # verificação se é vazio
            serializer = AtivoSerializer(instance=query, data=body)
            if serializer.is_valid():  # valida se o JSON pode ser serializado como ativo
                # res = serializer.update(instance=Ativo)

                # serializer.save()
                return Response(str(serializer.save(update_fields=['updated_at'])))
            else:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = AtivoSerializer(data=body)
            if serializer.is_valid():  # valida se o JSON pode ser serializado como ativo
                return Response(str(serializer.save()))
            else:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):  # verifica o banco
        queryset = Ativo.objects.all()  # busca os valores no banco
        permissions_classes = [
            permissions.AllowAny
        ]
        serializer = AtivoSerializer(
            queryset, many=True)  # convertendo em JSON
        return Response(serializer.data)  # valores do banco
