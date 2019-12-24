from django.test import TestCase
from .models import *
from .base import *
from .forms import *

# Create your tests here.

class UserTest(TestCase):
    def test_verificate(self):
        verificate(id=2)
        self.assertEqual(True,User.objects.get(id=2).isVerificated)

