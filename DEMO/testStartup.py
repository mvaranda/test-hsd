import demo_unittest, globalObjects

class TestStartup(demo_unittest.DemoTestCase):

    def setUp(self):
        self.val = 1
        self.log ("setUp for TestStartup was called.")

    def tearDown(self):
        self.log ("tearDown for TestStartup was called.")

    ################################################

    def testCheck01(self):
        """
            This is the TestStartup check 1 test.
        """
        globalObjects.mcduSim = "This is a global Obj" 
        self.log ("body of TestStartup testCheck01")
        self.assertEqual(1,1,"should work fine")
        self.warning("This is a warning sample")
        self.log ("end of body of TestStartup testCheck01")

    def testCheck02(self):
        """
            This is the TestStartup check 2 test.
        """
        self.log ("body of TestStartup testCheck02")
        self.assertEqual(1,2,"should Fail")
        self.log ("end of body of TestStartup testCheck02")

