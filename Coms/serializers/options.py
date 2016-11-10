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


class QueueExtras(serializers.ModelSerializer):
    size = serializers.IntegerField(write_only=True, required=False)
    # reference = serializers.IntegerField(write_only=True)

    class Meta(object):
        model = models.QueueExtras
        fields = ('id', 'size', 'reference', 'name', 'price', 'extra_character_price', 'description')


class QueueSizes(serializers.ModelSerializer):
    extras = QueueExtras(source="queueextras_set", many=True)
    type = serializers.IntegerField(write_only=True, required=False)
    # reference = serializers.IntegerField(write_only=True)

    class Meta(object):
        model = models.QueueSizes
        fields = ('id', 'type', 'reference', 'name', 'price', 'extra_character_price', 'description', 'extras')

    def create(self, validated_data):
        extras = validated_data.pop('queueextras_set')
        obj = self.Meta.model(**validated_data)
        print(validated_data)
        print(obj)
        obj.save()
        for extra in extras:
            extra['size'] = obj
            QueueExtras().create(extra)
        return obj


class QueueTypes(serializers.ModelSerializer):
    sizes = QueueSizes(source="queuesizes_set", many=True)
    queue = serializers.UUIDField(source="queue.id", required=False)
    # reference = serializers.IntegerField(write_only=True)

    class Meta(object):
        model = models.QueueTypes
        fields = ('id', 'queue', 'reference', 'name', 'price', 'extra_character_price', 'description', 'sizes',)

    def create(self, validated_data):
        sizes = validated_data.pop('queuesizes_set')
        obj = self.Meta.model(**validated_data)
        print(validated_data)
        print(obj)
        obj.save()
        for size in sizes:
            size['type'] = obj
            QueueSizes().create(size)
        return obj
