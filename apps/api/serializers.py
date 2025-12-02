from rest_framework import serializers
from apps.gestion_inventario.models import Comuna

class ComunaSerializer(serializers.ModelSerializer):
    """
    Serializador simple para el modelo Comuna.
    Solo expone los campos 'id' y 'nombre', que es lo que necesita el frontend.
    """
    class Meta:
        model = Comuna
        fields = ['id', 'nombre']




class ProductoLocalInputSerializer(serializers.Serializer):
    productoglobal_id = serializers.IntegerField(required=True)
    sku = serializers.CharField(required=True, max_length=100)
    es_serializado = serializers.BooleanField(default=False)
    es_expirable = serializers.BooleanField(default=False)