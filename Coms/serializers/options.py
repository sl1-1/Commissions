from rest_framework import serializers

import Coms.models as models


class OptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=200)
    price = serializers.DecimalField(decimal_places=2, max_digits=5, default=0.00)
    extra_character_price = serializers.DecimalField(decimal_places=2, max_digits=5, default=0.0)
    description = serializers.CharField(required=False, allow_blank=True, max_length=500)

    def update(self, instance, validated_data):
        validated_data.pop('id', None)
        super(OptionSerializer, self).update(instance, validated_data)


class TypeSerializer(OptionSerializer):
    class Meta(object):
        model = models.Type
        fields = ('id', 'name', 'price', 'extra_character_price', 'description')


class SizeSerializer(OptionSerializer):
    class Meta(object):
        model = models.Size
        fields = ('id', 'name', 'price', 'extra_character_price', 'description')


class ExtraSerializer(OptionSerializer):
    class Meta(object):
        model = models.Extra
        fields = ('id', 'name', 'price', 'extra_character_price', 'description')
