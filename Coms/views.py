from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
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

import models
import serializers.commission
import serializers.options
import serializers.queue
import serializers.user
from Coms import permissions


def csrf(request):
    """Hack so we can get our CSRF cookie into the angular app"""
    return HttpResponse('csrf')


class OptionViewSet(viewsets.ModelViewSet):
    """Setup the defaults for our option viewsets"""
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    filter_fields = ('id', 'disabled')
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)


class TypeViewSet(OptionViewSet):
    serializer_class = serializers.options.TypeSerializer
    queryset = models.Type.objects.all()


class SizeViewSet(OptionViewSet):
    serializer_class = serializers.options.SizeSerializer
    queryset = models.Size.objects.all()


class ExtraViewSet(OptionViewSet):
    serializer_class = serializers.options.ExtraSerializer
    queryset = models.Extra.objects.all()


class QueueViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.queue.QueueSerializer
    queryset = models.Queue.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    filter_fields = ('id',)
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)

    # def get_serializer_class(self):
    #     """Return the correct serializer if it is a read or write operation"""
    #     if self.action in ('list', 'retrieve'):
    #         return serializers.queue.QueueSerializerJson
    #     else:
    #         return serializers.queue.QueueWriteSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated():
            if user.is_staff or user.is_superuser:
                self.queryset = models.Queue.objects.all()
        else:
            self.queryset = models.Queue.objects.filter(hidden=False)
        return super(QueueViewSet, self).list(request, *args, **kwargs)


class ListFilter(Filter):
    """Thanks https://github.com/carltongibson/django-filter/issues/137 !"""

    @staticmethod
    def sanitize(value_list):
        """
        remove empty items in case of ?number=1,,2
        """
        return [v for v in value_list if v != u'']

    def filter(self, qs, value):
        value_list = value.split(u',')
        value_list = self.sanitize(value_list)
        return super(ListFilter, self).filter(qs, Lookup(value_list, 'in'))


class DateTimeRangeField(RangeField):
    """Django Filters do not support ISO 8601 date/time. This fixes that."""

    def __init__(self, *args, **kwargs):
        fields = (
            IsoDateTimeField(),
            IsoDateTimeField())
        super(DateTimeRangeField, self).__init__(fields, *args, **kwargs)


class DateTimeFromToRangeFilter(RangeFilter):
    """Django Filters do not support ISO 8601 date/time. This fixes that."""
    field_class = DateTimeRangeField


class CommissionViewSetFilter(filters.FilterSet):
    """Sets up our filters for the CommissionViewSet"""
    queue = ListFilter(name='queue')
    type = ListFilter(name='type')
    size = ListFilter(name='size')
    extras = ListFilter(name='extras')
    paid = ListFilter(name='paid')
    status = ListFilter(name='status')
    characters = RangeFilter(name='characters')
    date = DateTimeFromToRangeFilter(name='date')
    user = ListFilter(name='user__username')

    class Meta(object):
        model = models.Commission
        fields = ['queue', 'type', 'size', 'extras', 'paid', 'status', 'characters', 'date', 'user']


class CommissionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.commission.CommissionReadSerializer
    queryset = models.Commission.objects.all()
    filter_backends = (filters.DjangoObjectPermissionsFilter, filters.DjangoFilterBackend,)
    filter_class = CommissionViewSetFilter
    permission_classes = (permissions.CustomObjectPermissions,)
    filter_fields = ('id', 'queue', 'type', 'size', 'extras', 'paid', 'status', 'user')

    def get_serializer_class(self):
        """Return the correct serializer if it is a read or write operation"""
        if self.action in ('list', 'retrieve'):
            return serializers.commission.CommissionReadSerializer
        else:
            return serializers.commission.CommissionWriteSerializer

    def get_queryset(self):
        """Override the queryset, so that users can only see their own commissions"""
        user = self.request.user

        if self.action == 'list':
            if user.is_authenticated():
                if user.is_staff or user.is_superuser:
                    return models.Commission.objects.all().exclude(details_date__isnull=True)
                else:
                    return models.Commission.objects.filter(user=user).exclude(details_date__isnull=True)
            else:
                return models.Commission.objects.none()

        else:
            if user.is_authenticated():
                if user.is_staff or user.is_superuser:
                    return models.Commission.objects.all()
                else:
                    return models.Commission.objects.filter(user=user)
            else:
                return models.Commission.objects.none()

    def create(self, request, *args, **kwargs):
        """Override the default create login, as we need to validate some things"""
        if 'queue' not in request.data:
            raise ValidationError(detail="Queue must be set")
        if not request.data['queue']:
            raise ValidationError(detail="Queue must be set")

        queue = models.Queue.objects.get(pk=request.data['queue'])
        existing = queue.existing(request.user)
        if existing:
            return Response(serializers.commission.CommissionReadSerializer(existing).data)
        elif queue.is_full or queue.ended or queue.usermax(request.user):
            # Todo GIVE BETTER ERROR
            raise PermissionDenied(detail="You aren't allowed!")
        else:
            new = queue.commission_set.create(user=request.user)
            return Response(serializers.commission.CommissionReadSerializer(new).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # refresh the instance from the database.
            instance = self.get_object()
            serializer = self.get_serializer(instance)

        update = serializer.data
        print(update)
        return Response(update)


class CommissionFileViewSet(viewsets.ModelViewSet):
    # Todo: Rewrite this
    serializer_class = serializers.commission.CommissionFileSerializer
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
    serializer_class = serializers.user.UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        """Overrides the queryset to make sure only Admins can see all users"""
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)

    @list_route()
    def current(self, request):
        print(request.user)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @list_route(methods=['post'])
    def login(self, request):
        """Perform a login"""
        # TODO: Add some protection to this
        if 'username' not in request.data or 'password' not in request.data:
            return Response(data="Invalid Username or Password", status=403)
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
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @list_route(methods=['post'])
    def register(self, request):
        """Our Registration method"""
        # TODO: recaptcha?
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        if email and User.objects.filter(email=email).count() > 0:
            return Response(data='{"email": "Email Already used"}', status=403)
        if username and User.objects.filter(username=username).count() > 0:
            return Response(data='{"username": "Username already taken"}', status=403)

        # Add user to the correct group
        user = User.objects.create_user(username, email, password)
        group = Group.objects.get(name="Commissioners")
        user.groups.add(group)

        # Log them in after registration
        user = authenticate(username=username, password=password)
        login(request, user)
        return Response(serializers.user.UserSerializer(user).data)
