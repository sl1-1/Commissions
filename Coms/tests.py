from django.test import TestCase
import Coms.models as models
from time import sleep
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
