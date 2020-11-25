from rest_framework import serializers
from ativos.models import Ativo, Symbol


class AtivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ativo
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     instance['stocks'] = validated_data['stocks']
    #     instance.save()
    #     return instance


class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = '__all__'
