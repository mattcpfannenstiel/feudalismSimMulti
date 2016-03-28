import unittest

from Load import Load
from Lord import Lord
from Grain import Grain
from Fief import Fief
from LandUnit import LandUnit

class Test_Load(unittest.TestCase):
    """
    Test the load class to make sure it performs its job properly
    """

    def __init__(self, *args, **kwargs):
        super(Test_Load, self).__init__(*args, **kwargs)
        self.run = Load("Test", False)

    def setUp(self):
        print ("Set up")

    def tearDown(self):
        print ("Tear down")

    def test_initalize(self):
