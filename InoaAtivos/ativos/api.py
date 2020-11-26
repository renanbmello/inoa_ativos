from ativos.models import Ativo, Symbol
from rest_framework import viewsets, permissions, status
import requests
from .serializers import AtivoSerializer, SymbolSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from ativos.threads import GetAtivo
from threading import Event


class AtivoViewSet (viewsets.ModelViewSet):
    @action(detail=False, methods=['get'])  # escolhendo o metodo
    def get_ativo_data(self, request):
        permissions_classes = [
            permissions.AllowAny
        ]

        query = Ativo.objects.all()

        serializer = AtivoSerializer(
            query, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['get'])  # escolhendo o metodo
    def save_ativo_data(self, request):
        permissions_classes = [
            permissions.AllowAny
        ]

        erros = []

        symbols = Symbol.objects.all()
        symbolSerializer = SymbolSerializer(symbols, many=True)
        if not symbolSerializer.data:
            return Response({"message": "Não há ativos sendo observados."})

        threadList = []

        for symbol in symbolSerializer.data:
            thread = GetAtivo(symbol, erros)
            threadList.append(thread)

        for thread in threadList:
            thread.start()

        for thread in threadList:
            thread.join()

        if len(erros) != 0:
            return Response({"erros": erros})
        return Response("Sucesso")

    @action(detail=False, methods=['post'])  # escolhendo o metodo
    def add_new_ativo(self, request):
        permissions_classes = [
            permissions.AllowAny
        ]

        try:
            query = Symbol.objects.get(name=request.data["name"])

            if query != None:
                return Response(data={"message": "Ativo já monitorado"})

        except Exception as erro:
            None
            # return Response(str(erro), status=status.HTTP_404_NOT_FOUND)

        serializer = SymbolSerializer(data=request.data)

        if serializer.is_valid():  # valida se o JSON pode ser serializado como ativo
            res = serializer.save()
            return Response(str(res))
        else:

            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['delete'])  # escolhendo o metodo
    def delete_ativo(self, request):
        permissions_classes = [
            permissions.AllowAny
        ]

        try:
            instance = Symbol.objects.get(id=request.GET["id"])

            instance.delete()
            return Response(data={"message": "Ativo deletado"})

        except Exception as erro:
            return Response(str(erro))

    @action(detail=False, methods=['get'])
    def list_ativos(self, request):  # verifica o banco
        queryset = Ativo.objects.all()  # busca os valores no banco
        permissions_classes = [
            permissions.AllowAny
        ]
        serializer = AtivoSerializer(
            queryset, many=True)  # convertendo em JSON
        return Response(serializer.data)  # valores do banco
