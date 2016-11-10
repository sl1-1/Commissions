from rest_framework import serializers

import Coms.models as models
import Coms.serializers.options as options


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
    types = options.TypeSerializer(many=True)
    sizes = options.SizeSerializer(many=True)
    extras = options.ExtraSerializer(many=True)
