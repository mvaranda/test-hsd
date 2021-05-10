import sys
import unittest
import time
import demo_test_reports

class DemoTestCase(unittest.TestCase):
    """A class whose instances are single test cases.

    By default, the test code itself should be placed in a method named
    'runTest'.

    If the fixture may be used for many test cases, create as
    many test methods as are needed. When instantiating such a TestCase
    subclass, specify in the constructor arguments the name of the test method
    that the instance is to execute.

    Test authors should subclass TestCase for their own tests. Construction
    and deconstruction of the test's environment ('fixture') can be
    implemented by overriding the 'setUp' and 'tearDown' methods respectively.

    If it is necessary to override the __init__ method, the base class
    __init__ method must always be called. It is important that subclasses
    should not change the signature of their __init__ method, since instances
    of the classes are instantiated automatically by parts of the framework
    in order to be run.
    """

    # This attribute determines which exception will be raised when
    # the instance's assertion methods fail; test methods raising this
    # exception will be deemed to have 'failed' rather than 'errored'

    failureException = AssertionError

    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)
        self._result = None

    def run(self, result=None):
        if result is None: self._result = None
        else: self._result = result
        unittest.TestCase.run(self, result)

    def log( self, text ):
        if self._result is None: return
        self._result.log(self, text)

    def warning( self, text ):
        if self._result is None: return
        self._result.warning(self, text)
        


class DemoTestResult(unittest.TestResult):
    """A test result class that can print formatted text results to a stream.
    """
    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self, testConfig, log=0):
        unittest.TestResult.__init__(self)
        self.testConfig = testConfig
        self.stream = sys.stdout
        self._log = log
        self._lastTestClassProcessed = ""
        self.htmlReportBuilder = demo_test_reports.htmlReportBuilder(testConfig)

    def _getTestClassName( self, test ):
        r = test.id().split(".")
        return r[1] 

    def _getTestCaseName( self, test ):
        r = test.id().split(".")
        return r[2] 

    def log( self, test, text ):
        #print "LOG:    " + test.id() + text
        print "Log :   " + self._getTestClassName(test) + "." + self._getTestCaseName(test) + ": " + text

        self.htmlReportBuilder.addTestCaseEntry ( self._getTestClassName(test), self._getTestCaseName(test), "Log", text )

    def warning( self, test, text ):
        print "Warning:" + self._getTestClassName(test) + "." + self._getTestCaseName(test) + ": " + text
        self.htmlReportBuilder.addTestCaseEntry ( self._getTestClassName(test), self._getTestCaseName(test), "Warning", text )


    def getDescription(self, test):
        if 1:
            return test.shortDescription() or str(test)
        else:
            return str(test)

    def startTest(self, test):
        unittest.TestResult.startTest(self, test)
        if self._log != 0: print "*** startTest Called class: ", self._getTestClassName( test )

    def stopTest(self, test):
        unittest.TestResult.stopTest(self, test)
        if self._log != 0: print "*** stopTest Called"

    def _correctFilename(self, filename):
        if filename[-4:] in ('.pyc', '.pyo'):
            return filename[:-1]
        return filename

    def _printProgress(self):
        if self._log != 0: 
            total = self.testsRun
            errors = len(self.errors)
            failures = len(self.failures)
            success = total - errors - failures
            print "*** Num Tests Run so far = ", total
            print "*** Num Success so far = ", success
            print "*** Num failures so far = ", failures
            print "*** Num errors so far = ", errors

            
    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        print "Pass:   " + self._getTestClassName(test) + "." + self._getTestCaseName(test) + ": "

        if self._log != 0: print "*** addSuccess called test: ",test
        self.htmlReportBuilder.addTestCaseEntry ( self._getTestClassName(test), self._getTestCaseName(test), "Pass", "Pass" )
        self._printProgress()
        
    def addError(self, test, err):
        print "Error:  " + self._getTestClassName(test) + "." + self._getTestCaseName(test) + ": " + self._exc_info_to_string(err, test)

        unittest.TestResult.addError(self, test, err)
        if self._log != 0: print "*** addError called"
        self.htmlReportBuilder.addTestCaseEntry ( self._getTestClassName(test), self._getTestCaseName(test), "Error", self._exc_info_to_string(err, test) )
        self._printProgress()

    def addFailure(self, test, err):
        print "Fail:   " + self._getTestClassName(test) + "." + self._getTestCaseName(test) + ": " + self._exc_info_to_string(err, test)
        unittest.TestResult.addFailure(self, test, err)
        if self._log != 0: print "*** addFailure called"
        self.htmlReportBuilder.addTestCaseEntry ( self._getTestClassName(test), self._getTestCaseName(test), "Failure", self._exc_info_to_string(err, test) )
        self._printProgress()

    def _createSummaryReport(self):
        total = self.testsRun
        errors = len(self.errors)
        failures = len(self.failures)
        warnings = 3
        demo_test_reports.create_summary_page (self.testConfig, total, warnings, failures, errors, "now", "1:00")

    def closeReports(self):
        self.htmlReportBuilder.close()

    def deployReports(self):
        self.htmlReportBuilder.deployReports()

    def printErrors(self):
        if self._log != 0: print "*** printErrors called"
        self._printProgress()
        self.stream.write("\n")
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)


    def printErrorList(self, flavour, errors):
        for test, err in errors:
            self.stream.write(self.separator1)
            self.stream.write("\n%s: %s\n" % (flavour,self.getDescription(test)))
            self.stream.write(self.separator2)
            self.stream.write("\n%s\n" % err)

class DemoTestRunner:
    """A test runner class that displays results in textual form.

    It prints out the names of tests as they are run, errors as they
    occur, and a summary of the results at the end of the test run.
    """
    def __init__(self, testDir):
        self.testDir = testDir

    def run(self, test):
        "Run the given test case or test suite."
        result = DemoTestResult(self.testDir)
        startTime = time.time()
        test(result)
        stopTime = time.time()
        timeTaken = float(stopTime - startTime)
        result.closeReports()
        result.printErrors()
        result.deployReports()
        return result


