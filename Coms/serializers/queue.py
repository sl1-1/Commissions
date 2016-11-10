from rest_framework import serializers

import Coms.models as models
import Coms.serializers.options as options


class QueueSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)
    open = serializers.SerializerMethodField()
    submissions_by_user = serializers.SerializerMethodField()
    full = serializers.SerializerMethodField()
    existing = serializers.SerializerMethodField()
    types = options.QueueTypes(source="queuetypes_set", many=True)

    class Meta(object):
        model = models.Queue
        fields = ('id', 'name', 'date', 'max_characters', 'max_commissions_in_queue',
                  'max_commissions_per_person', 'expire', 'closed', 'hidden', 'start', 'end', 'submission_count',
                  'open', 'submissions_by_user', 'full', 'ended', 'existing', 'types')

    def create(self, validated_data):
        types = validated_data.pop('queuetypes_set')
        obj = models.Queue(**validated_data)
        obj.save()
        for item in types:
            item['queue'] = obj
            print(item)
            options.QueueTypes().create(item)
        print(obj)
        return obj

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
