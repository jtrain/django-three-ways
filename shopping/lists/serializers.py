from rest_framework import serializers

from lists.models import List, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'quantity')


class ListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = List
        fields = ('name', 'items', 'created_at', 'url')

    def get_url(self, obj):
        return obj.get_absolute_url()

    def create(self, validated_data):
        items = validated_data.pop('items')
        shopping_list = List.objects.create(**validated_data)
        for item in items:
            item['belongs_to_id'] = shopping_list.id
            Item.objects.create(**item)
        return shopping_list

