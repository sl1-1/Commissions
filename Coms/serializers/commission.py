import decimal
import json
import logging

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CreateOnlyDefault
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

import Coms.models as models
import Coms.serializers.options as options

logger = logging.getLogger('Coms')


class CommissionFileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    commission = serializers.CharField()
    imgname = serializers.CharField(read_only=True)
    token = serializers.CharField(write_only=True)
    thumb = HyperlinkedSorlImageField(
        '600',
        options={"crop": "center"},
        source='img',
        read_only=True)

    class Meta(object):
        model = models.CommissionFiles
        fields = ('id', 'user', 'commission', 'date', 'imgname', 'img', 'token', 'thumb')

    def create(self, validated_data):
        commission = models.Commission.objects.get(pk=validated_data.pop('commission'))
        message = commission.message_set.filter(token=validated_data.pop('token')).first()
        com_file = models.CommissionFiles(commission=commission, message=message, **validated_data)
        com_file.save()
        return com_file


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    status_changes = serializers.SerializerMethodField()
    commissionfiles_set = CommissionFileSerializer(many=True, required=False)
    token = serializers.CharField(write_only=True)

    class Meta(object):
        model = models.Message
        fields = ('id', 'user', 'date', 'type', 'message', 'status_changes', 'commissionfiles_set', 'token')

    @staticmethod
    def get_status_changes(obj):
        try:
            if obj.status_changes:
                return json.loads(obj.status_changes)
            else:
                return {}
        except ValueError:
            logger.debug('Error in Message ID {}'.format(obj.id))


class CommissionReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    status = serializers.SerializerMethodField()
    paid = serializers.SerializerMethodField()
    queue_name = serializers.SerializerMethodField()
    type = options.TypeSerializer()
    size = options.SizeSerializer()
    characters = serializers.IntegerField(default=CreateOnlyDefault(0))
    extras = options.ExtraSerializer(many=True)
    message_set = MessageSerializer(many=True)

    class Meta(object):
        model = models.Commission
        fields = ('id', 'user', 'date', 'locked', 'status', 'paid', 'submitted', 'expired', 'message_set',
                  'type', 'size', 'extras', 'characters', 'queue', 'queue_name', 'details_date')

    def __init__(self, *args, **kwargs):
        self.show_history = kwargs.pop('history', True)
        super(CommissionReadSerializer, self).__init__(*args, **kwargs)

    @staticmethod
    def get_status(obj):
        return obj.status, obj.get_status_display()

    @staticmethod
    def get_paid(obj):
        return obj.paid, obj.get_paid_display()

    @staticmethod
    def get_queue_name(obj):
        return obj.queue.name


class DecimalEncoder(json.JSONEncoder):
    # http://stackoverflow.com/a/3885198
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


# noinspection PyMethodMayBeStatic
class CommissionWriteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    message = MessageSerializer(required=False)

    class Meta(object):
        model = models.Commission
        fields = ('id', 'user', 'date', 'locked', 'submitted', 'expired', 'message',
                  'type', 'size', 'extras', 'characters', 'queue', 'details_date', 'status', 'paid')

    # noinspection PyUnusedLocal
    def validate_details_date(self, value):
        if not self.instance.details_date:
            return timezone.now()
        return self.instance.details_date

    def update(self, instance, validated_data):
        original = dict(CommissionReadSerializer(instance).data)
        print()
        print(original)
        print(validated_data)

        if 'message' in validated_data:
            message = message = models.Message(user=self.context['request'].user, commission=instance,
                                               **validated_data.pop('message'))
        else:
            message = message = models.Message(user=self.context['request'].user, commission=instance, token='')

        updated = super(CommissionWriteSerializer, self).update(instance, validated_data)
        up = dict(CommissionReadSerializer(updated).data)
        original.pop('message_set')
        original.pop('date')
        original.pop('details_date')
        status_changes = {}
        for k in original.keys():
            if original[k] != up[k]:
                status_changes[k] = {'old': original[k], 'new': up[k]}

        if status_changes:
            # Work around json field chocking on decimals
            status_changes = json.dumps(status_changes, cls=DecimalEncoder)
            print(status_changes)
            message.status_changes = status_changes
            message.type = 1
        if message:
            if not updated.message_set.count():
                message.type = 0
            message.save()
        print(type(updated))
        return updated

    def validate_characters(self, value):
        if value > self.instance.queue.max_characters:
            raise serializers.ValidationError(
                "Characters must be less than {}".format(self.instance.queue.max_characters))
        return value

    def validate_type(self, value):
        if value not in self.instance.queue.queuetypes_set.all():
            raise ValidationError('{id} is not valid'.format(id=value.id))
        return value

    def validate(self, data):
        if data['size'] not in data['type'].queuesizes_set.all():
            raise ValidationError('Specified size not avalilble with this type')
        if any(extra not in data['size'].queueextras_set.all() for extra in data['extras']):
            raise ValidationError('Specified extra(s) not avalilble with this size')
        return data

    def validate_status(self, value):
        """
        Check that the user has permission to change this
        If they don't, keep it as it was
        :param value:
        :return:
        """
        print('Is staff?', self.context['request'].user.is_staff)
        if self.context['request'].user.is_staff:
            return value
        else:
            return self.instance.status

    def validate_paid(self, value):
        """
        Check that the user has permission to change this.
        If they don't, keep it as it was
        :param value:
        :return:
        """
        print('Is staff?', self.context['request'].user.is_staff)
        if self.context['request'].user.is_staff:
            return value
        else:
            return self.instance.paid
