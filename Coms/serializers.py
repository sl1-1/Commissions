import decimal
import json

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import metadata
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CreateOnlyDefault

import models

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class CustomMetaData(metadata.SimpleMetadata):
    def determine_metadata(self, request, view):
        data = super(CustomMetaData, self).determine_metadata(request, view)
        data['table'] = view.table
        return data


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


class SizeSerializer(OptionSerializer):
    class Meta(object):
        model = models.Size


class ExtraSerializer(OptionSerializer):
    class Meta(object):
        model = models.Extra


class QueueReadSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(style={'base_template': 'date.html'}, required=False)
    end = serializers.DateTimeField(style={'base_template': 'date.html'}, required=False)
    open = serializers.SerializerMethodField()
    submissions_by_user = serializers.SerializerMethodField()
    full = serializers.SerializerMethodField()
    existing = serializers.SerializerMethodField()

    class Meta(object):
        model = models.Queue
        fields = ('id', 'name', 'date', 'types', 'sizes', 'extras', 'max_characters', 'max_commissions_in_queue',
                  'max_commissions_per_person', 'expire', 'closed', 'hidden', 'start', 'end', 'submission_count',
                  'open', 'submissions_by_user', 'full', 'ended', 'existing')

    @staticmethod
    def get_open(obj):
        return not obj.ended

    def get_submissions_by_user(self, obj):
        if self.context['request'].user.is_authenticated():
            return obj.user_submission_count(self.context['request'].user)

    @staticmethod
    def get_full(obj):
        return obj.is_full

    def get_existing(self, obj):
        if self.context['request'].user.is_authenticated():
            existing = obj.existing(self.context['request'].user)
            if existing:
                return existing.id
            else:
                return None


class QueueWriteSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(required=True)
    end = serializers.DateTimeField(required=False)

    class Meta(object):
        model = models.Queue
        fields = ('id', 'name', 'date', 'types', 'sizes', 'extras', 'max_characters', 'max_commissions_in_queue',
                  'max_commissions_per_person', 'expire', 'closed', 'hidden', 'start', 'end')


class QueueSerializerJson(QueueReadSerializer):
    types = TypeSerializer(many=True)
    sizes = SizeSerializer(many=True)
    extras = ExtraSerializer(many=True)


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    status_changes = serializers.SerializerMethodField()

    class Meta(object):
        model = models.Message
        fields = ('id', 'user', 'date', 'type', 'message', 'status_changes')

    @staticmethod
    def get_status_changes(obj):
        try:
            return json.loads(obj.status_changes)
        except ValueError as e:
            logger.error(e, obj.status_changes)


class CommissionReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    status = serializers.SerializerMethodField()
    paid = serializers.SerializerMethodField()
    queue_name = serializers.SerializerMethodField()
    type = TypeSerializer()
    size = SizeSerializer()
    characters = serializers.IntegerField(default=CreateOnlyDefault(0))
    extras = ExtraSerializer(many=True)
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
        message = None
        if 'message' in validated_data:
            message = models.Message(user=self.context['request'].user,
                                     commission=instance,
                                     **validated_data.pop('message'))

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
            if not message:
                message = models.Message(user=self.context['request'].user, commission=instance, message="")
            message.status_changes = status_changes
            message.type = 1
        if message:
            if not updated.message_set.count():
                message.type = 0
            message.save()
        return updated

    def validate_characters(self, value):
        if value > self.instance.queue.max_characters:
            raise serializers.ValidationError(
                "Characters must be less than {}".format(self.instance.queue.max_characters))
        return value

    def validate_type(self, value):
        if value not in self.instance.queue.types.all():
            raise ValidationError('{id} is not valid'.format(id=value.id))
        return value

    def validate_size(self, value):
        print(type(value))
        if value not in self.instance.queue.sizes.all():
            raise ValidationError('{id} is not valid'.format(id=value.id))
        return value

    def validate_extras(self, value):
        valid_extras = self.instance.queue.extras.all()
        for extra in value:
            print(dir(extra))
            if extra not in valid_extras:
                raise ValidationError('{id} is not valid'.format(id=extra.id))
        return value

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


class CommissionFileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    imgname = serializers.CharField(read_only=True)

    class Meta(object):
        model = models.CommissionFiles
        fields = ('id', 'user', 'commission', 'date', 'note', 'imgname', 'img', 'user_deleted', 'deleted')


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'is_active')
