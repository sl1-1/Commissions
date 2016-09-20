from django.utils import timezone
from rest_framework import filters
from rest_framework import serializers, viewsets

import models


# noinspection PyMethodMayBeStatic
class CharacterSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    date = serializers.SerializerMethodField()

    class Meta(object):
        model = models.Character
        fields = ('id', 'user', 'name', 'description', 'img', 'date', 'friendlyid')

    def get_date(self, obj):
        return timezone.localtime(obj.date)


class CommissionViewSet(viewsets.ModelViewSet):
    serializer_class = CharacterSerializer
    queryset = models.Character.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'user', 'name')
