from collections import OrderedDict

from rest_framework import serializers, viewsets
from rest_framework import filters
from django.utils import timezone
from rest_framework.renderers import JSONRenderer, HTMLFormRenderer, BrowsableAPIRenderer
from rest_framework import metadata
from rest_framework.response import Response

import models


# noinspection PyMethodMayBeStatic,PyMethodMayBeStatic,PyMethodMayBeStatic
class CommissionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    date = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    paid_display = serializers.SerializerMethodField()

    class Meta(object):
        model = models.Commission
        fields = ('id', 'user', 'date', 'locked', 'status', 'paid', 'price_adjustment', 'details_submitted', 'expired',
                  'latest_detail', 'status_display', 'paid_display', 'queue')

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_paid_display(self, obj):
        return obj.get_paid_display()

    def get_date(self, obj):
        return timezone.localtime(obj.date).strftime("%Y-%m-%d %H:%M:%S %Z")


class CommissionViewSet(viewsets.ModelViewSet):
    serializer_class = CommissionSerializer
    queryset = models.Commission.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'queue')


class CustomMetaData(metadata.SimpleMetadata):
    def determine_metadata(self, request, view):
        data = super(CustomMetaData, self).determine_metadata(request, view)
        data['table'] = view.table
        return data


class OptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    price = serializers.DecimalField(decimal_places=2, max_digits=5, default=0.00, style={'base_template': 'number.html'})
    extra_character_price = serializers.DecimalField(decimal_places=2, max_digits=5, default=0.0,
                                                     style={'base_template': 'number.html'})
    description = serializers.CharField(required=False, allow_blank=True, max_length=500)


class OptionViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'disabled')
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer,)
    metadata_class = CustomMetaData
    table = OrderedDict([('name', 'Name'), ('price', 'Price'), ('extra_character_price', 'Extra Character Price'),
                         ('description', 'Description')])

    def list(self, request, *args, **kwargs):
        if type(request.accepted_renderer) == HTMLFormRenderer:
            serializer = self.get_serializer()
            return Response(serializer.data)
        else:
            return super(OptionViewSet, self).list(request, *args, **kwargs)


class TypeSerializer(OptionSerializer):
    class Meta(object):
        model = models.Type


class TypeViewSet(OptionViewSet):
    serializer_class = TypeSerializer
    queryset = models.Type.objects.all()


class SizeSerializer(OptionSerializer):
    class Meta(object):
        model = models.Size


class SizeViewSet(OptionViewSet):
    serializer_class = SizeSerializer
    queryset = models.Size.objects.all()


class ExtraSerializer(OptionSerializer):
    class Meta(object):
        model = models.Type


class ExtraViewSet(OptionViewSet):
    serializer_class = ExtraSerializer
    queryset = models.Extra.objects.all()


class ContactMethodSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.ContactMethod


class ContactMethidViewSet(OptionViewSet):
    serializer_class = ContactMethodSerializer
    queryset = models.ContactMethod.objects.all()
    table = OrderedDict([('name', 'Name'), ('description', 'Description')])
