from django.utils import timezone
from rest_framework import filters
from rest_framework import metadata
from rest_framework import serializers, viewsets
from rest_framework.renderers import JSONRenderer, HTMLFormRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse

import models


class TemplateHTMLFormRenderer(TemplateHTMLRenderer):
    format = 'form'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        renderer_context = renderer_context or {}
        view = renderer_context['view']
        request = renderer_context['request']
        response = renderer_context['response']
        data = {'serializer': data.serializer, 'data': data}
        template_names = self.get_template_names(response, view)
        template = self.resolve_template(template_names)

        context = self.resolve_context(data, request, response)
        return template.render(context)


class CustomMetaData(metadata.SimpleMetadata):
    def determine_metadata(self, request, view):
        data = super(CustomMetaData, self).determine_metadata(request, view)
        data['table'] = view.table
        return data


# noinspection PyMethodMayBeStatic
class QueueSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(style={'base_template': 'date.html'}, required=False)
    end = serializers.DateTimeField(style={'base_template': 'date.html'}, required=False)
    date = serializers.SerializerMethodField()
    open = serializers.SerializerMethodField()
    enter_url = serializers.SerializerMethodField()

    class Meta(object):
        model = models.Queue
        fields = ('id', 'name', 'date', 'types', 'sizes', 'extras', 'max_characters', 'max_commissions_in_queue',
                  'max_commissions_per_person', 'expire', 'closed', 'hidden', 'start', 'end', 'submission_count',
                  'open', 'enter_url')

    def get_date(self, obj):
        return timezone.localtime(obj.date).strftime("%Y-%m-%d %H:%M:%S %Z")

    def get_open(self, obj):
        return not obj.ended

    def get_enter_url(self, obj):
        return reverse('Coms:Enter:View', args=[obj.id], request=self.context.get('request'))


class QueueViewSet(viewsets.ModelViewSet):
    serializer_class = QueueSerializer
    queryset = models.Queue.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id',)
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, TemplateHTMLFormRenderer)
    template_name = 'Coms/ajax/Option.html'
    metadata_class = CustomMetaData
    table = {
        'cols': [
            {'title': 'Name', 'className': 'queuelink', 'data': 'name'},
            {'data': 'date', 'title': 'Created'},
            {'data': 'max_commissions_in_queue', 'title': 'Max Commissions'},
            {'data': 'submission_count', 'title': 'Submissions in Queue'},
            {'data': 'open', 'title': 'Open', 'className': 'iconbool'},
            {'data': 'enter_url', 'title': 'Link', 'className': 'iconlink'}
        ],
        'order': "date"}

    def list(self, request, *args, **kwargs):
        if type(request.accepted_renderer) == HTMLFormRenderer:
            serializer = self.get_serializer()
            return Response(serializer.data)
        else:
            return super(QueueViewSet, self).list(request, *args, **kwargs)


# noinspection PyMethodMayBeStatic
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
    metadata_class = CustomMetaData
    table = {
        'cols': [
            {'title': 'Username', 'data': 'user', 'className': 'modallink'},
            {'title': 'Submitted', 'data': 'date'},
            {'title': 'Details Submitted', 'data': 'details_submitted', 'className': 'iconbool'},
            {'title': 'Status', 'data': 'status_display'},
            {'title': 'Paid', 'data': 'paid_display'},
            {'title': 'Locked', 'data': 'locked', 'className': 'iconlock'}
        ],
        'order': "date"}


class OptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    price = serializers.DecimalField(decimal_places=2, max_digits=5, default=0.00,
                                     style={'base_template': 'number.html'})
    extra_character_price = serializers.DecimalField(decimal_places=2, max_digits=5, default=0.0,
                                                     style={'base_template': 'number.html'})
    description = serializers.CharField(required=False, allow_blank=True, max_length=500)


class OptionViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('id', 'disabled')
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, TemplateHTMLFormRenderer)
    metadata_class = CustomMetaData
    template_name = 'Coms/ajax/Option.html'
    table = {'cols': [
        {'title': 'Name', 'className': 'modallink', 'data': 'name'},
        {'data': 'price', 'title': 'Price'},
        {'data': 'extra_character_price', 'title': 'Extra Character Price'},
        {'data': 'description', 'title': 'Description'}
    ]}

    def list(self, request, *args, **kwargs):
        if type(request.accepted_renderer) == TemplateHTMLFormRenderer:
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


class ContactMethodViewSet(OptionViewSet):
    serializer_class = ContactMethodSerializer
    queryset = models.ContactMethod.objects.all()
    table = {'cols': [
        {'title': 'Name', 'className': 'modallink', 'data': 'name'},
        {'data': 'description', 'title': 'Description'}
    ]}
