import uuid

from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta


class Option(models.Model):
    class Meta:
        abstract = True

    def __unicode__(self):
        return self.friendly

    def __str__(self):
        return self.friendly

    @property
    def friendly(self):
        if self.price != 0.00:
            return "{} - ${}".format(self.name, self.price)
        else:
            return self.name


class Type(Option):
    class Meta:
        verbose_name = "Commission Type"

    name = models.CharField(max_length=200)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=5)
    description = models.CharField(max_length=500, blank=True)
    disabled = models.BooleanField(default=False)


class Size(Option):
    class Meta:
        verbose_name = "Commission Size"

    name = models.CharField(max_length=200)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=5)
    description = models.CharField(max_length=500, blank=True)
    disabled = models.BooleanField(default=False)


class Extra(Option):
    class Meta:
        verbose_name = "Commission Extra"

    name = models.CharField(max_length=200)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=5)
    description = models.CharField(max_length=500, blank=True)
    disabled = models.BooleanField(default=False)


class QueueManager(models.Manager):
    @property
    def openqueues(self):
        return self.get_queryset().filter(closed=False).filter(models.Q(hidden=False) | models.Q(end__isnull=True))


class Queue(models.Model):
    objects = QueueManager()

    class Meta:
        verbose_name = "Commission Queue"

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
    end = models.DateTimeField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('Coms:queue', args=(self.id,))

    @property
    def submission_count(self):
        if self.expire > 0:
            expiry = now() - timedelta(minutes=self.expire)
            query = self.commission_set.filter(date__gt=expiry) | self.commission_set.filter(detail__isnull=False)
            return query.count()
        else:
            return self.commission_set.count()

    @property
    def open_slots(self):
        return self.max_commissions_in_queue - self.submission_count

    @property
    def percent_full(self):
        return self.submission_count / float(self.max_commissions_in_queue) * 100

    @property
    def is_full(self):
        if self.submission_count >= self.max_commissions_in_queue:
            return True
        else:
            return False

    @property
    def ended(self):
        if self.closed:
            return True
        elif self.end is not None and self.end < now():
            return True
        else:
            return False

    @property
    def show(self):
        if not self.hidden and not self.ended:
            return True
        else:
            return False

    def user_submission_count(self, user):
        expiry = now() - timedelta(minutes=self.expire)
        query = self.commission_set.filter(user=user).filter(date__gt=expiry) | \
            self.commission_set.filter(user=user).filter(detail__isnull=False)
        return query.count()


class ContactMethod(models.Model):
    class Meta:
        verbose_name = "Contact Method"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    message_url = models.URLField(blank=True)
    profile_url = models.URLField(blank=True)
    description = models.CharField(max_length=500, blank=True)
    disabled = models.BooleanField(default=False)


class Commission(models.Model):
    # def __unicode__(self):
    #     return self.user.username
    #
    # def __str__(self):
    #     return self.user.username

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
    price_adjustment = models.DecimalField(default=0.00, decimal_places=2, max_digits=5)

    @property
    def details_submitted(self):
        return bool(self.detail_set.count())

    @property
    def expired(self):
        expiry = self.date + timedelta(minutes=self.queue.expire)
        if expiry < now():
            return True
        else:
            return False



class Contact(models.Model):
    def __unicode__(self):
        return '{}: {}'.format(self.site.name, self.username)

    def __str__(self):
        return '{}: {}'.format(self.site.name, self.username)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site = models.ForeignKey(ContactMethod)
    commission = models.ForeignKey(Commission)
    username = models.CharField(max_length=100)
    primary = models.BooleanField(default=False)

    @property
    def get_profile(self):
        profile = self.site.profile_url.format(username=self.username)

        return profile

    @property
    def get_message(self):
        message = self.site.message_url.format(username=self.username)
        return message


class Detail(models.Model):
    class Meta:
        verbose_name = "Commission Detail"

    def __unicode__(self):
        return str(self.pk)

    def __str__(self):
        return str(self.pk)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.ForeignKey(Type)
    size = models.ForeignKey(Size)
    number_of_Characters = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    extras = models.ManyToManyField(Extra, blank=True)
    details = models.TextField(max_length=10000)
    primary_contact = models.ForeignKey(Contact, blank=True, null=True, related_name="detail_pc")
    date = models.DateTimeField('Details Submitted', auto_now_add=True)
    com = models.ForeignKey(Commission)
    contacts = models.ManyToManyField(Contact, blank=True)
    paypal = models.EmailField()
