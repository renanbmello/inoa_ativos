from rest_framework import serializers
from ativos.models import Ativo


class AtivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ativo
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     instance['stocks'] = validated_data['stocks']
    #     instance.save()
    #     return instance
