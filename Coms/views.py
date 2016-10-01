from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core import serializers as dserializers
from django.http import HttpResponse
from django_filters import Filter
from django_filters.fields import Lookup, RangeField, IsoDateTimeField
from django_filters.filters import RangeFilter
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from reversion import revisions as reversion
from reversion.revisions import transaction

import models
import serializers
from Coms import permissions


def csrf(request):
    return HttpResponse('csrf')


# noinspection PyUnresolvedReferences
class ReversionViewMixin(object):
    def dispatch(self, *args, **kwargs):
        with transaction.atomic(), reversion.create_revision():
            response = super(ReversionViewMixin, self).dispatch(*args, **kwargs)
            if not self.request.user.is_anonymous():
                reversion.set_user(self.request.user)
            return response


class OptionViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoObjectPermissionsFilter, filters.DjangoFilterBackend,)
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    filter_fields = ('id', 'disabled')
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)


class TypeViewSet(OptionViewSet):
    serializer_class = serializers.TypeSerializer
    queryset = models.Type.objects.all()


class SizeViewSet(OptionViewSet):
    serializer_class = serializers.SizeSerializer
    queryset = models.Size.objects.all()


class ExtraViewSet(OptionViewSet):
    serializer_class = serializers.ExtraSerializer
    queryset = models.Extra.objects.all()


class QueueViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.QueueSerializerJson
    queryset = models.Queue.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    filter_fields = ('id',)
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.QueueSerializerJson
        else:
            return serializers.QueueWriteSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated():
            if user.is_staff or user.is_superuser:
                self.queryset = models.Queue.objects.all()
        else:
            self.queryset = models.Queue.objects.filter(hidden=False)
        return super(QueueViewSet, self).list(request, *args, **kwargs)


# noinspection PyUnusedLocal
class CommissionHistoryViewSet(viewsets.ViewSet):
    # TODO: Secure me!
    serializer_class = serializers.CommissionReadSerializer
    queryset = models.Commission.objects.all()

    # noinspection PyUnusedLocal, PyMethodMayBeStatic
    def list(self, request, commissions_pk=None):
        obj = models.Commission.objects.get(pk=commissions_pk)
        versions = list(reversion.get_for_object(obj).get_unique())
        versions.reverse()
        return Response([{'date': x.revision.date_created, 'id': index} for index, x in enumerate(versions)])

    # noinspection PyUnusedLocal, PyMethodMayBeStatic
    def retrieve(self, request, pk=None, commissions_pk=None):
        pk = int(pk)
        obj = models.Commission.objects.get(pk=commissions_pk)
        versions = list(reversion.get_for_object(obj).get_unique())
        versions.reverse()
        historical = dserializers.deserialize('json', versions[pk].serialized_data,
                                              ignorenonexistent=True).next().object
        historical.date = obj.date
        historical.details_date = obj.details_date
        return Response(serializers.CommissionReadSerializer(historical, history=False).data)


class ListFilter(Filter):
    """
    Thanks https://github.com/carltongibson/django-filter/issues/137 !
    """

    def sanitize(self, value_list):
        """
        remove empty items in case of ?number=1,,2
        """
        return [v for v in value_list if v != u'']

    def filter(self, qs, value):
        value_list = value.split(u',')
        value_list = self.sanitize(value_list)
        return super(ListFilter, self).filter(qs, Lookup(value_list, 'in'))


class DateTimeRangeField(RangeField):
    """
    Django Filters do not support ISO 8601 date/time. This fixes that.
    """
    def __init__(self, *args, **kwargs):
        fields = (
            IsoDateTimeField(),
            IsoDateTimeField())
        super(DateTimeRangeField, self).__init__(fields, *args, **kwargs)


class DateTimeFromToRangeFilter(RangeFilter):
    """
    Django Filters do not support ISO 8601 date/time. This fixes that.
    """
    field_class = DateTimeRangeField


class CommissionViewSetFilter(filters.FilterSet):
    queue = ListFilter(name='queue')
    type = ListFilter(name='type')
    size = ListFilter(name='size')
    extras = ListFilter(name='extras')
    paid = ListFilter(name='paid')
    status = ListFilter(name='status')
    characters = RangeFilter(name='characters')
    date = DateTimeFromToRangeFilter(name='date')

    class Meta:
        model = models.Commission
        fields = ['queue', 'type', 'size', 'extras', 'paid', 'status', 'characters', 'date']


class CommissionViewSet(ReversionViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.CommissionReadSerializer
    queryset = models.Commission.objects.all()
    filter_backends = (filters.DjangoObjectPermissionsFilter, filters.DjangoFilterBackend,)
    filter_class = CommissionViewSetFilter
    permission_classes = (permissions.CustomObjectPermissions,)
    filter_fields = ('id', 'queue', 'type', 'size', 'extras', 'paid', 'status')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.CommissionReadSerializer
        else:
            return serializers.CommissionWriteSerializer

    def initial(self, request, *args, **kwargs):
        # print(request.data)
        super(CommissionViewSet, self).initial(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated():
            if user.is_staff or user.is_superuser:
                return models.Commission.objects.all()
            else:
                return models.Commission.objects.filter(user=user)
        else:
            return models.Commission.objects.none()

    @list_route()
    def ego(self, request):
        user = request.user
        print(user)
        if user.is_authenticated():
            serializer = serializers.CommissionReadSerializer(models.Commission.objects.filter(user=user), many=True)
        else:
            serializer = serializers.CommissionReadSerializer(models.Commission.objects.none(), many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if 'queue' not in request.data:
            raise ValidationError(detail="Queue must be set")
        if not request.data['queue']:
            raise ValidationError(detail="Queue must be set")

        queue = models.Queue.objects.get(pk=request.data['queue'])
        existing = queue.existing(request.user)
        if existing:
            return Response(serializers.CommissionReadSerializer(existing).data)
        elif queue.is_full or queue.ended or queue.usermax(request.user):
            # Todo GIVE BETTER ERROR
            raise PermissionDenied(detail="You aren't allowed!")
        else:
            new = queue.commission_set.create(user=request.user)
            return Response(serializers.CommissionReadSerializer(new).data)

    def list(self, request, queues_pk=None, **kwargs):
        if queues_pk:
            qs = models.Commission.objects.filter(queue=queues_pk)
            if not (request.user.is_staff or request.user.is_superuser):
                qs.filter(user=request.user)
            return Response(serializers.CommissionReadSerializer(qs.all(), many=True).data)
        else:
            return super(CommissionViewSet, self).list(request, **kwargs)


class CommissionFileViewSet(ReversionViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.CommissionFileSerializer
    queryset = models.CommissionFiles.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (permissions.CustomObjectPermissions,)
    filter_fields = ('id', 'commission')

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated():
            if user.is_staff or user.is_superuser:
                return models.CommissionFiles.objects.all()
            else:
                return models.CommissionFiles.objects.filter(user=user)
        else:
            return models.CommissionFiles.objects.none()

    def perform_create(self, serializer):
        filename = self.request.FILES['img'].name
        serializer.save(user=self.request.user, imgname=filename)

    def perform_destroy(self, instance):
        if self.request.user.is_staff:
            instance.deleted = True
        else:
            instance.user_deleted = True
        instance.save()

    @list_route()
    def ego(self, request):
        user = request.user
        if user.is_authenticated():
            serializer = self.get_serializer(models.CommissionFiles.objects.filter(user=user), many=True)
        else:
            serializer = self.get_serializer(models.CommissionFiles.objects.none(), many=True)
        return Response(serializer.data)


# todo RESTRICT THIS!
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)

    @list_route()
    def current(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @list_route(methods=['post'])
    def login(self, request):
        """
        TODO: FUCKING PROTECT THIS
        :param request:
        :return:
        """
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        else:
            return Response(data="Invalid Username or Password", status=403)

    @list_route(methods=['get'])
    def logout(self, request):
        logout(request)
        return Response("")


class ContactMethodViewSet(OptionViewSet):
    serializer_class = serializers.ContactMethodSerializer
    queryset = models.ContactMethod.objects.all()
