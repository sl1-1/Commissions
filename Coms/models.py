import uuid
from datetime import timedelta

from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from guardian.shortcuts import assign_perm
from os import path


class Option(models.Model):
    """
    An Abstract model for some shared methods in Type, Size, Extra models.
    """

    class Meta(object):
        abstract = True

    def __unicode__(self):
        return self.friendly

    def __str__(self):
        return self.friendly

    @property
    def friendly(self):
        """
        Gets a more friendly name for our objects
        :return: string
        """
        if self.price != 0.00:
            return "{0} - ${1}".format(self.name, self.price)
        else:
            return self.name


class Type(Option):
    """
    Type model, holds the various commission types
    """

    class Meta(object):
        verbose_name = "Commission Type"
        default_permissions = ('view',)

    name = models.CharField(max_length=200)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=5)
    extra_character_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=5)
    description = models.CharField(max_length=500, blank=True)
    disabled = models.BooleanField(default=False)


class Size(Option):
    """
    Size model, holds the various commission sizes
    """

    class Meta(object):
        verbose_name = "Commission Size"
        default_permissions = ('view',)

    name = models.CharField(max_length=200)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=5)
    extra_character_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=5)
    description = models.CharField(max_length=500, blank=True)
    disabled = models.BooleanField(default=False)


class Extra(Option):
    """
    Extra model, holds the various commission extras
    """

    class Meta(object):
        verbose_name = "Commission Extra"
        default_permissions = ('view',)

    name = models.CharField(max_length=200)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=5)
    extra_character_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=5)
    description = models.CharField(max_length=500, blank=True)
    disabled = models.BooleanField(default=False)


class QueueManager(models.Manager):
    """
    Manager for Queue model, mainly used for showing open queues on index
    """

    @property
    def openqueues(self):
        """
        Gets our open queues
        :return: ``django.db.models.query.QuerySet``
        """
        return self.get_queryset().filter(closed=False).filter(models.Q(hidden=False) | models.Q(end__isnull=True))


class Queue(models.Model):
    """
    Queue Model, holds the different queues
    """
    objects = QueueManager()

    class Meta(object):
        verbose_name = "Commission Queue"
        default_permissions = ('view',)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    date = models.DateTimeField('date created', auto_now_add=True)
    types = models.ManyToManyField(Type)
    sizes = models.ManyToManyField(Size)
    max_characters = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    character_cost = models.DecimalField(default=0.00, decimal_places=2, max_digits=5)
    extras = models.ManyToManyField(Extra, blank=True)
    max_commissions_in_queue = models.IntegerField(default=1)
    max_commissions_per_person = models.IntegerField(default=1)
    expire = models.IntegerField(default=15)
    closed = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    end = models.DateTimeField(blank=True, null=True, default=None)
    start = models.DateTimeField(default=now)

    @property
    def submission_count(self):
        """
        Counts the submissions in this queue, excluding expired submissions
        :return: integer
        """
        if self.expire > 0:
            expiry = now() - timedelta(minutes=self.expire)
            query = self.commission_set.filter(date__gt=expiry) | self.commission_set.filter(details_date__isnull=False)
            return query.distinct('id').count()
        else:
            return self.commission_set.distinct('id').count()

    @property
    def open_slots(self):
        """
        Gets the amount of slots left for this queue
        :return: integer
        """
        return self.max_commissions_in_queue - self.submission_count

    @property
    def percent_full(self):
        """
        Calculates how full this queue is in percent
        :return: float
        """
        return self.submission_count / float(self.max_commissions_in_queue) * 100

    @property
    def is_full(self):
        """
        Returns True if queue is full, otherwise returns False
        :return: boolean
        """
        if self.submission_count >= self.max_commissions_in_queue:
            return True
        else:
            return False

    @property
    def ended(self):
        """
        Returns True if the queue has ended, otherwise returns False
        :return: Boolean
        """
        if self.max_commissions_in_queue == 0:
            return True
        if self.closed:
            return True
        elif self.start > now() or self.end is not None and self.end < now():
            return True
        else:
            return False

    @property
    def show(self):
        """
        Returns True if the queue should be shown, otherwise returns False
        :return: boolean
        """
        if not self.hidden and not self.ended:
            return True
        else:
            return False

    def user_submission_count(self, user):
        """
        When given the user, returns a count of submissions they have in the queue
        :param user:
        :return: integer
        """
        expiry = now() - timedelta(minutes=self.expire)
        query = self.commission_set.filter(user=user).filter(date__gt=expiry) | \
            self.commission_set.filter(user=user).filter(details_date__isnull=False)
        return query.count()

    def existing(self, user):
        existing = self.commission_set.filter(user=user).filter(details_date__isnull=True).first()
        if existing:
            return existing

    def usermax(self, user):
        return self.user_submission_count(user) >= self.max_commissions_per_person


class ContactMethod(models.Model):
    """
    ContactMethod Model, Holds our contact methods
    """

    class Meta(object):
        verbose_name = "Contact Method"
        default_permissions = ('view',)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    message_url = models.URLField(blank=True)
    profile_url = models.URLField(blank=True)
    description = models.CharField(max_length=500, blank=True)
    disabled = models.BooleanField(default=False)

    @property
    def profile(self):
        """
        Returns ``str.format`` of the profile_url field
        :return: ``str.format`` method
        """
        return self.profile_url.format

    @property
    def message(self):
        """
        Returns ``str.format`` of the profile_url field
        :return: ``str.format`` method
        """
        return self.message_url.format


class Commission(models.Model):
    """
    Commission Model, Holds all the important bits for each commission
    """

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, blank=True, null=True, default=None)
    queue = models.ForeignKey(Queue)
    date = models.DateTimeField('Submitted', auto_now_add=True)
    locked = models.BooleanField(default=False)
    status_choices = ((0, 'Waiting'), (1, 'Sketched'), (2, 'Lined'), (3, 'Coloured'),
                      (4, 'Finished'), (5, 'Canceled'), (6, 'Please Revise'), (7, 'Rejected'))
    status = models.IntegerField(choices=status_choices, default=0)
    paid_choices = ((0, 'Not Yet Requested'), (1, 'Invoiced'), (2, 'Paid'), (3, 'Refunded'))
    paid = models.IntegerField(choices=paid_choices, default=0)

    type = models.ForeignKey(Type, blank=True, null=True, default=None)
    size = models.ForeignKey(Size, blank=True, null=True, default=None)
    characters = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    extras = models.ManyToManyField(Extra, blank=True)
    details_date = models.DateTimeField('Details Submitted', null=True)
    submitted = models.BooleanField(default=False)

    class Meta:
        default_permissions = ('add', 'view', 'change')

    @property
    def total(self):
        """
        Totals all the options on the commission, and returns it.
        :return: cost as a floating point value
        """
        characters = self.characters - 1
        cost = self.type.price
        cost += self.type.extra_character_price * characters
        cost += self.size.price
        cost += self.size.extra_character_price * characters
        for extra in self.extras.all():
            cost += extra.price
            cost += extra.extra_character_price * characters
        return cost

    @property
    def expired(self):
        """
        Check if commission has expired
        :return: Boolean
        """
        expiry = self.date + timedelta(minutes=self.queue.expire)
        if expiry < now() and not self.submitted:
            return True
        else:
            return False


class UserData(models.Model):
    user = models.ForeignKey(User)
    sites = JSONField(default=list)


class Message(models.Model):
    user = models.ForeignKey(User)
    commission = models.ForeignKey(Commission)
    date = models.DateTimeField('Sent', auto_now_add=True)
    type_choices = ((0, 'Initial'), (1, 'Reply'), (2, 'Status Update'))
    type = models.IntegerField(choices=type_choices, default=2)
    message = models.TextField(max_length=10000, blank=True, default='')
    status_changes = models.TextField()

    class Meta:
        default_permissions = ('add', 'view', 'change')


def file_name(instance, filename):
    user = instance.user.id
    return path.join(str(user), 'wip', str(uuid.uuid4()), filename)


class CommissionFiles(models.Model):
    """
    Commission Files Model, Holds our file uploads for commissions.
    """

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    commission = models.ForeignKey(Commission)
    user = models.ForeignKey(User)
    imgname = models.CharField(max_length=1000)
    img = models.ImageField(upload_to=file_name)
    user_deleted = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    message = models.ForeignKey(Message)

    class Meta:
        default_permissions = ('add', 'view', 'change')


# noinspection PyUnusedLocal
@receiver(post_save, sender=Commission)
def commission_post_save(sender, **kwargs):
    print(kwargs)
    commission, created = kwargs["instance"], kwargs["created"]
    if created:
        assign_perm("view_commission", commission.user, commission)
        assign_perm("change_commission", commission.user, commission)


# noinspection PyUnusedLocal
@receiver(post_save, sender=CommissionFiles)
def commissionfiles_post_save(sender, **kwargs):
    print(kwargs)
    commissionfile, created = kwargs["instance"], kwargs["created"]
    if created:
        assign_perm("view_commissionfiles", commissionfile.user, commissionfile)
        assign_perm("change_commissionfiles", commissionfile.user, commissionfile)
