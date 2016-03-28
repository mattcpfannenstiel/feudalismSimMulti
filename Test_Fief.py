import unittest
from Fief import Fief
from Grain import Grain
from LandUnit import LandUnit
from Lord import Lord


class Test_Fief(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test_Fief, self).__init__(*args, **kwargs)
        self.test_fief0 = Fief(0, 6, False)
        self.test_fief1 = Fief(1, 7, False)
        self.test_fmap = []
        self.test_lord0 = None
        self.test_lord1 = None

    def setUp(self):
        print ("Set up")
        self.test_fmap = self.makemap(4, 2)
        x = 0
        while x < 4:
            y = 0
            while y < 2:
                if x < 2:
                    land0 = LandUnit(x, y, self.test_fief0, False)
                    self.test_fief0.containedLand.append(land0)
                    land0.addserf()
                    self.test_fmap[x][y].append(x)
                    self.test_fmap[x][y].append(y)
                    self.test_fmap[x][y].append(land0)
                    self.test_fmap[x][y].append(1)

                else:
                    land1 = LandUnit(x, y, self.test_fief1, False)
                    land1.addserf()
                    self.test_fief1.containedLand.append(land1)
                    self.test_fmap[x][y].append(x)
                    self.test_fmap[x][y].append(y)
                    self.test_fmap[x][y].append(land1)
                    self.test_fmap[x][y].append(1)

                y += 1
            x += 1
        self.test_lord0 = Lord("Lord 0", self.test_fief0, False)
        self.test_fief0.ruler = self.test_lord0
        self.test_lord1 = Lord("Lord 1", self.test_fief1, False)
        self.test_fief1.ruler = self.test_lord1
        self.test_fief0.stores = Grain(self.test_fief0)
        self.test_fief1.stores = Grain(self.test_fief1)

    def tearDown(self):
        print ("Tear down")

    def test_find_borders(self):
        print("Starting find borders test")
        self.test_fief0.findborders(self.test_fmap, 4, 2)
        self.test_fief1.findborders(self.test_fmap, 4, 2)
        self.assertEqual(len(self.test_fief0.containedLand), len(self.test_fief1.containedLand),
                         "Land count is not the same")
        self.assertEqual(len(self.test_fief1.attackoptions), 2, "Length of attack options isn't 2 for fief 1")
        self.assertEqual(len(self.test_fief0.attackoptions), 2, "Length of attack options isn't 2 for fief 0")

    def test_remove_land(self):
        print("Starting remove land test")
        self.test_fief0.removeland(0, 0)
        self.test_fief1.removeland(3, 0)
        self.assertEqual(len(self.test_fief0.containedLand), 3, "Land was not removed from fief 0")
        self.assertEqual(len(self.test_fief1.containedLand), 3, "Land was not removed from fief 1")

    def test_remove_attack_option(self):
        print ("Starting attack option test")
        self.test_fief1.findborders(self.test_fmap, 4, 2)
        self.test_fief0.findborders(self.test_fmap, 4, 2)
        self.test_fief0.removeattackoption(2, 0)
        self.test_fief1.removeattackoption(1, 1)
        self.assertEqual(len(self.test_fief0.attackoptions), 1, "Attack option not removed from fief 0")
        self.assertEqual(len(self.test_fief1.attackoptions), 1, "Attack option not removed from fief 1")

    def test_find_upkeep(self):
        print ("Start upkeep test")
        test0 = self.test_fief0.findupkeep()
        test1 = self.test_fief1.findupkeep()
        self.assertEqual(test1, 20, "Upkeep amount isn't correct for fief 1")
        self.assertEqual(test0, 20, "Upkeep amount isn't correct for fief 0")

    def test_place_serf(self):
        print ("Start place serf")
        self.test_fief0.placeserf()
        self.test_fief1.placeserf()
        self.assertEqual(self.test_fief0.serf_number, 1, "Serf number didn't incriment in fief 0")
        self.assertEqual(self.test_fief1.serf_number, 1, "Serf number didn't incriment in fief 1")

    def test_calculate_wealth(self):
        print("Start wealth calculate")
        self.test_fief0.calculatewealth()
        self.test_fief1.calculatewealth()
        self.assertEqual(self.test_fief0.stores.getwealth(), 180,
                         "The production in fief 0 was not calculated correctly")
        self.assertEqual(self.test_fief1.stores.getwealth(), 180,
                         "The production in fief 1 was not calculated correctly")

    def test_all_land_full(self):
        print ("Start land all full test")
        x = 0
        self.assertEqual(len(self.test_fief0.containedLand), 4, "Length of fief 0 contained land isnt 4")
        self.assertEqual(len(self.test_fief1.containedLand), 4, "Length of fief 1 contained land isnt 4")
        while x < 4:
            self.test_fief0.containedLand[x].full = True
            x += 1
        temp0 = self.test_fief0.alllandfull()
        temp1 = self.test_fief1.alllandfull()
        self.assertEqual(temp0, True, "All land is not full in fief 0")
        self.assertEqual(temp1, False, "All land is full in fief 1")

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(self.test_find_borders())
        suite.addTest(self.test_remove_land())
        suite.addTest(self.test_remove_attack_option())
        suite.addTest(self.test_find_upkeep())
        suite.addTest(self.test_place_serf())
        suite.addTest(self.test_calculate_wealth())
        suite.addTest(self.test_all_land_full())
        return suite

    def runTest(self):
        t = Test_Fief()
        suite = t.suite()

    def makemap(self, width, height):
        fmap = []
        i = 0
        while i < width:
            j = 0
            fmap.append([])
            while j < height:
                fmap[i].append([])
                j += 1
            i += 1
        return fmap
