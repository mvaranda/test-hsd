import demo_unittest, globalObjects

class TestMcduPhoneBook(demo_unittest.DemoTestCase):

    def setUp(self):
        self.val = 1
        self.log ("setUp for TestMcduPhoneBook was called.")

    def tearDown(self):
        self.log ("tearDown for TestMcduPhoneBook was called.")

    ################################################

    def testCheck01(self):
        """
            This is the TestMcduPhoneBook check 1 test.
        """
        self.log ("body of TestMcduPhoneBook testCheck01")
        self.assertEqual(1,1,"should work fine")
        self.log ("end of body of TestMcduPhoneBook testCheck01")

    def testCheck02(self):
        """
            This is the TestMcduPhoneBook check 2 test.
        """
        self.log ("body of TestMcduPhoneBook testCheck02")
        self.assertEqual(1,2,"should Fail")
        self.log ("end of body of TestMcduPhoneBook testCheck02")

class TestMcduPhoneBook02(demo_unittest.DemoTestCase):

    def setUp(self):
        self.val = 1
        self.log ("setUp for TestMcduPhoneBook02 was called.")

    def tearDown(self):
        self.log ("tearDown for TestMcduPhoneBook02 was called.")

    ################################################

    def testCheck01(self):
        """
            This is the TestMcduPhoneBook02 check 1 test.
        """
        self.log ("body of TestMcduPhoneBook02 testCheck01")
        self.warning( "Test Global: " + globalObjects.mcduSim )
        self.assertEqual(1,1,"should work fine")
        self.log ("end of body of TestMcduPhoneBook02 testCheck01")

    def testCheck02(self):
        """
            This is the TestMcduPhoneBook02 check 2 test.
        """
        self.log ("body of TestMcduPhoneBook02 testCheck02")
        self.assertEqual(1,2,"should Fail")
        self.log ("end of body of TestMcduPhoneBook02 testCheck02")

