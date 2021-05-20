from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        models = [StockProduct(stock=stock, **pos) for pos in positions]
        StockProduct.objects.bulk_create(models)

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        for pos in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=pos['product'],
                defaults={
                    'price': pos['price'],
                    'quantity': pos['quantity'],
                },
            )
        StockProduct.objects.filter(stock=stock).exclude(
            product__in={p['product'] for p in positions}
        ).delete()

        return stock
