from django.test import TestCase
import Coms.models as models
from time import sleep
from django.utils import timezone
from datetime import timedelta
# Create your tests here.


class QueueIsFullExpire(TestCase):
    expire = 15
    max_commissions = 5

    def setUp(self):
        self.test_type = models.Type.objects.create(name="Test Type")
        self.test_size = models.Size.objects.create(name="test size")
        self.test_extra = models.Extra.objects.create(name="test extra")

    def testbasic(self):
        queue = models.Queue.objects.create(name='Test Case 1', max_characters=1,
                                            max_commissions_in_queue=self.max_commissions,
                                            max_commissions_per_person=10, expire=self.expire)
        queue.types.add(self.test_type)
        queue.sizes.add(self.test_size)
        queue.extras.add(self.test_extra)
        for i in range(0, self.max_commissions - 1):
            models.Commission.objects.create(queue=queue)
            self.assertEqual(queue.is_full, False)
        models.Commission.objects.create(queue=queue)
        self.assertEqual(queue.is_full, True)

    def testexpire(self):
        queue = models.Queue.objects.create(name='Test Case 2', max_characters=1,
                                            max_commissions_in_queue=self.max_commissions,
                                            max_commissions_per_person=10, expire=1)
        queue.types.add(self.test_type)
        queue.sizes.add(self.test_size)
        queue.extras.add(self.test_extra)
        for i in range(0, self.max_commissions - 1):
            models.Commission.objects.create(queue=queue)
            self.assertEqual(queue.is_full, False)
        models.Commission.objects.create(queue=queue)
        self.assertEqual(queue.submission_count, queue.max_commissions_in_queue)
        self.assertEqual(queue.is_full, True)
        sleep(61)
        self.assertEqual(queue.is_full, False)
        self.assertEqual(queue.submission_count, 0)


class QueueTestEnded(TestCase):
    expire = 15
    max_commissions = 5

    def setUp(self):
        self.test_type = models.Type.objects.create(name="Test Type")
        self.test_size = models.Size.objects.create(name="test size")
        self.test_extra = models.Extra.objects.create(name="test extra")

    def testbasic(self):
        queue = models.Queue.objects.create(name='Test Case 1', max_characters=1,
                                            max_commissions_in_queue=self.max_commissions,
                                            max_commissions_per_person=10, expire=1)
        self.assertEqual(queue.ended, False)

        queue.closed = True
        self.assertEqual(queue.ended, True)
        queue.closed = False
        self.assertEqual(queue.ended, False)

        queue.max_commissions_in_queue = 0
        self.assertEqual(queue.ended, True)
        queue.max_commissions_in_queue = 3
        self.assertEqual(queue.ended, False)

    def testtime(self):
        endtime = timezone.now() + timedelta(0, 5)
        queue = models.Queue.objects.create(name='Test Case 1', max_characters=1,
                                            max_commissions_in_queue=self.max_commissions,
                                            max_commissions_per_person=10, expire=1, end=endtime)

        self.assertEqual(queue.ended, False)
        while timezone.now() < endtime:
            pass
        self.assertEqual(queue.ended, True)


class QueueTestShow(TestCase):
    expire = 1
    max_commissions = 5

    def setUp(self):
        self.test_type = models.Type.objects.create(name="Test Type")
        self.test_size = models.Size.objects.create(name="test size")
        self.test_extra = models.Extra.objects.create(name="test extra")

    def testShow(self):
        queue = models.Queue.objects.create(name='Test Case 1', max_characters=1,
                                            max_commissions_in_queue=self.max_commissions,
                                            max_commissions_per_person=10, expire=1)
        self.assertEqual(queue.show, True)
        queue.hidden = True
        self.assertEqual(queue.show, False)
        queue.hidden = False
        self.assertEqual(queue.show, True)
        queue.closed = True
        self.assertEqual(queue.show, False)
        queue.closed = False
        self.assertEqual(queue.show, True)
        endtime = timezone.now() + timedelta(0, 5)
        queue.end = endtime
        self.assertEqual(queue.show, True)
        while timezone.now() < endtime:
            pass
        self.assertEqual(queue.show, False)







