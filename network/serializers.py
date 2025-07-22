from rest_framework import serializers
from .models import NetworkPoint, Contact, Product
from .validators import check_supplier_chain


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class NetworkPointSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(read_only=True)
    contact_id = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        write_only=True,
        source="contacts",
        required=False,
    )
    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True
    )
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=NetworkPoint.objects.all(), required=False
    )

    class Meta:
        model = NetworkPoint
        fields = [
            "id",
            "name",
            "level",
            "contacts",
            "contact_id",
            "products",
            "supplier",
            "debt",
            "created_at",
        ]
        read_only_fields = ["debt", "created_at"]

    def create(self, validated_data):
        """
        Создание нового объекта NetworkPoint, исключая поле 'debt' из данных.
        """
        validated_data.pop("debt", None)
        products_data = validated_data.pop("products")
        network_point = NetworkPoint(**validated_data)
        network_point.clean()
        network_point.save()
        network_point.products.set(products_data)
        return network_point

    def to_representation(self, instance):
        """Меняем вывод для GET-запросов, добавляем сериализацию продуктов."""
        data = super().to_representation(instance)
        if "products" in data:
            data["products"] = ProductSerializer(
                instance.products.all(), many=True
            ).data
        return data

    def validate(self, data):
        """
        Дополнительная проверка на валидность цепочки поставщиков.
        """
        level = data.get("level", getattr(self.instance, "level", None))
        supplier = data.get("supplier", getattr(self.instance, "supplier", None))

        if supplier:
            if not check_supplier_chain(data["supplier"]):
                raise serializers.ValidationError(
                    "Цепочка поставщиков не может быть более трех уровней."
                )

        if level != NetworkPoint.FACTORY and supplier is None:
            raise serializers.ValidationError(
                f"Необходимо указать поставщика для уровня '{level}'."
            )

        return data
