from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'description']



class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ('id', 'product', 'quantity', 'price')


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)


    # настройте сериализатор для склада
    class Meta:
        model = Stock
        fields = ('id', 'address', 'positions')

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = Stock.objects.create(**validated_data)


        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            StockProduct.objects.create(stock=stock, **position)

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        # for position in positions:
        #     items = StockProduct.objects.filter(stock=stock)
        #     for item in items:
        #         if item.product == position.get('product'):
        #             item.quantity = position.get('quantity')
        #             item.price = position.get('price')
        #             item.save()

        for item in positions:
            StockProduct. \
                objects.update_or_create(defaults={'quantity': item['quantity'],
                                                   'price': item['price']
                                                   },
                                         product=item['product'],
                                         stock=stock
                                         )
        return stock
