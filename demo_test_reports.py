import os, sys, time, emailsender, shutil


class htmlReportBuilder(  ):

    def __init__(self, testConfig):
        self._testConfig = testConfig

        self._totalNumTests = 0
        self._totalNumWarnings = 0
        self._totalNumFailures = 0
        self._totalNumErrors = 0
        self._startOverallTime = time.time()

        self._classNumTests = 0
        self._classNumWarnings = 0
        self._classNumFailures = 0
        self._classNumErrors = 0
        self._classStartTime = time.time()

        self._lastTestClassProcessed = ""
        self._ClassNamesList = []

        self._htmlDir = testConfig["http_dir"] + "/"  + testConfig["testID"]
        self._attachmentDir = self._htmlDir + "/attachments"
        os.mkdir(self._htmlDir)
        os.mkdir(self._attachmentDir)

        self._BodyFileName_Class = self._htmlDir + "/ClassReportBody.$$$"
        self._BodyFileName_AllTests = self._htmlDir + "/AllTestsBody.$$$"
        self._BodyFileName_WarningOnly = self._htmlDir + "/WarningOnlyBody.$$$"
        self._BodyFileName_FailureOnly = self._htmlDir + "/FailureOnlyBody.$$$"
        self._BodyFileName_ErrorOnly = self._htmlDir + "/ErrorOnlyBody.$$$"
        self._BodyFileName_Summary = self._htmlDir + "/SummaryBody.$$$"

        self._htmlFileName_summary = self._htmlDir + "/Summary.html"
        self._htmlFileName_AllTests = self._htmlDir + "/AllTests.html"
        self._htmlFileName_WarningOnly = self._htmlDir + "/WarningOnly.html"
        self._htmlFileName_FailureOnly = self._htmlDir + "/FailureOnly.html"
        self._htmlFileName_ErrorOnly = self._htmlDir + "/ErrorOnly.html"

        self._tempFile4ClassReportBody = None
        #self._tempFile4ClassReportBody = file(self._BodyFileName_Class, "wb" )
        self._tempFile4AllTestsReportBody = file(self._BodyFileName_AllTests, "wb" )
        self._tempFile4WarningOnlyReportBody = file(self._BodyFileName_WarningOnly, "wb" )
        self._tempFile4FailureOnlyReportBody = file(self._BodyFileName_FailureOnly, "wb" )
        self._tempFile4ErrorOnlyReportBody = file(self._BodyFileName_ErrorOnly, "wb" )
        self._tempFile4SummaryReportBody = file(self._BodyFileName_Summary, "wb" )
        #os.mkdir(testConfig["http_dir"])

    def _closeSummaryPage (self):
        top = summary_page__top
        testID = self._testConfig["testID"]
        #errorRate = (  (self._totalNumFailures + self._totalNumErrors) * 100) / self._totalNumTests
        errorRate = (  (self._totalNumTests - self._totalNumFailures - self._totalNumErrors) * 100) / self._totalNumTests
        timenow = time.time()
        ascTimeNow = time.strftime("%H:%M:%S", time.localtime(timenow)) 
        ascStartTime = time.strftime("%H:%M:%S", time.localtime(self._startOverallTime)) 
        duration = int(timenow - self._startOverallTime)
        top = top.replace("$$$TestName", self._testConfig["TestName"])
        top = top.replace("$$$DateAndTime", time.asctime() )
        top = top.replace("$$$LinkToAllTests", self._htmlFileName_AllTests.replace(self._htmlDir+"/",'') )
        top = top.replace("$$$LinkToAllWarnings", self._htmlFileName_WarningOnly.replace(self._htmlDir+"/",'') )
        top = top.replace("$$$LinkToAllFailures", self._htmlFileName_FailureOnly.replace(self._htmlDir+"/",'') )
        top = top.replace("$$$LinkToAllErrors", self._htmlFileName_ErrorOnly.replace(self._htmlDir+"/",'') )
        top = top.replace("$$$TotalNumTests", str(self._totalNumTests) )
        top = top.replace("$$$TotalNumWarnings", str(self._totalNumWarnings) )
        top = top.replace("$$$TotalNumFaillures", str(self._totalNumFailures) )
        top = top.replace("$$$TotalNumErrors", str(self._totalNumErrors) )
        top = top.replace("$$$SuccessRate", str(errorRate) )
        top = top.replace("$$$StartTime", ascStartTime)
        top = top.replace("$$$Duration", str(duration) )

        f = file(self._htmlFileName_summary, "w")
        f.write(top)

        self._tempFile4SummaryReportBody.close()
        self._tempFile4SummaryReportBody = file(self._BodyFileName_Summary, "rb" )
        body = self._tempFile4SummaryReportBody.read() 
        f.write( body )
        f.write( TestClass_page_botton )
        f.close ()
        self._tempFile4ClassReportBody.close()


    def _closeIndividualPape( self, ReportName, bodyFilename, bodyFile, htmlFilename ):
        top = individual_page__top
        testID = self._testConfig["testID"]
        errorRate = (  (self._totalNumTests - self._totalNumFailures - self._totalNumErrors) * 100) / self._totalNumTests
        #errorRate = (  (self._totalNumFailures + self._totalNumErrors) * 100) / self._totalNumTests
        timenow = time.time()
        ascTimeNow = time.strftime("%H:%M:%S", time.localtime(timenow)) 
        ascStartTime = time.strftime("%H:%M:%S", time.localtime(self._startOverallTime)) 
        duration = int(timenow - self._startOverallTime)
        top = top.replace("$$$TestName",  self._testConfig["TestName"])
        top = top.replace("$$$ReportType", ReportName)
        top = top.replace("$$$DateAndTime", time.asctime() )
        top = top.replace("$$$LinkToAllTests", self._htmlFileName_AllTests.replace(self._htmlDir+"/",'') )
        top = top.replace("$$$LinkToAllWarnings", self._htmlFileName_WarningOnly.replace(self._htmlDir+"/",'') )
        top = top.replace("$$$LinkToAllFailures", self._htmlFileName_FailureOnly.replace(self._htmlDir+"/",'') )
        top = top.replace("$$$LinkToAllErrors", self._htmlFileName_ErrorOnly.replace(self._htmlDir+"/",'') )
        top = top.replace("$$$TotalNumTests", str(self._totalNumTests) )
        top = top.replace("$$$TotalNumWarnings", str(self._totalNumWarnings) )
        top = top.replace("$$$TotalNumFaillures", str(self._totalNumFailures) )
        top = top.replace("$$$TotalNumErrors", str(self._totalNumErrors) )
        top = top.replace("$$$SuccessRate", str(errorRate) )
        top = top.replace("$$$StartTime", ascStartTime)
        top = top.replace("$$$Duration", str(duration) )

        f = file( htmlFilename, "w")
        f.write(top)

        bodyFile.close()
        bodyFile = file(bodyFilename, "rb" )
        body = bodyFile.read() 
        f.write( body )
        f.write( TestClass_page_botton )
        f.close ()
        bodyFile.close()

    def _closeAllTestsPage (self):
        self._closeIndividualPape( "All Tests", self._BodyFileName_AllTests, self._tempFile4AllTestsReportBody, self._htmlFileName_AllTests )

    def _closeWarningsOnlyPage (self):
        self._closeIndividualPape( "Warnings Only", self._BodyFileName_WarningOnly, self._tempFile4WarningOnlyReportBody, self._htmlFileName_WarningOnly )

    def _closeFailuresOnlyPage (self):
        self._closeIndividualPape( "Failures Only", self._BodyFileName_FailureOnly, self._tempFile4FailureOnlyReportBody, self._htmlFileName_FailureOnly )

    def _closeErrorsOnlyPage (self):
        self._closeIndividualPape( "Errors Only", self._BodyFileName_ErrorOnly, self._tempFile4ErrorOnlyReportBody, self._htmlFileName_ErrorOnly )

    def _closeTestClassReport( self ):
        #if self._tempFile4ClassReportBody.closed() == True: return
        if self._tempFile4ClassReportBody == None: return
        timenow = time.time()
        ascTimeNow = time.strftime("%H:%M:%S", time.localtime(timenow)) 
        duration = int(timenow - self._classStartTime)
        #successRate =  ((self._classNumFailures + self._classNumErrors) * 100) / self._classNumTests
        successRate =  ((self._classNumTests - self._classNumFailures - self._classNumErrors) * 100) / self._classNumTests
        top = TestClass_page_top
        top = top.replace("$$$TestClassName", self._lastTestClassProcessed)
        top = top.replace("$$$DateAndTime", time.asctime(time.localtime(timenow)) )
        #top = top.replace("$$$xxx", testID + "_AllTests.html")
        #top = top.replace("$$$LinkToAllWarnings", testID + "_AllWarnings.html" )
        top = top.replace("$$$NumTests", str(self._classNumTests) )
        top = top.replace("$$$NumWarnings", str(self._classNumWarnings) )
        top = top.replace("$$$NumFaillures", str(self._classNumFailures) )
        top = top.replace("$$$NumErrors", str(self._classNumErrors) )
        top = top.replace("$$$SuccessRate", str(successRate) )
        top = top.replace("$$$StartTime",   ascTimeNow )
        top = top.replace("$$$Duration", str(duration) )
        self._classStartTime = time.time()

        # create final class file
        outputFileName = self._htmlDir + "/Class_" + self._lastTestClassProcessed + ".html"
        f = file( outputFileName, "wb")
        f.write(top)
        self._tempFile4ClassReportBody.close()
        self._tempFile4ClassReportBody = file(self._BodyFileName_Class, "rb" )
        body = self._tempFile4ClassReportBody.read() 
        f.write( body )
        f.write( TestClass_page_botton )
        f.close ()
        self._tempFile4ClassReportBody.close()

        # lets add summary entry
        if self._classNumErrors > 0:
            entryType = "Error"
        elif self._classNumFailures > 0:
            entryType = "Failuire"
        elif self._classNumWarnings > 0:
            entryType = "Warning"
        else:
            entryType = "Pass"

        entry = summary_page__entry
        entry = entry.replace("$$$EntryType", entryType)
        entry = entry.replace("$$$TestClassName", self._lastTestClassProcessed)
        entry = entry.replace("$$$LinkToTestClass", outputFileName.replace(self._htmlDir+"/",'') )
        entry = entry.replace("$$$PkgNumTests", str(self._classNumTests) )
        entry = entry.replace("$$$PkgNumWarnings", str(self._classNumWarnings) )
        entry = entry.replace("$$$PkgNumFailures", str(self._classNumFailures) )
        entry = entry.replace("$$$PkgNumErrors", str(self._classNumErrors) )
        entry = entry.replace("$$$PkgStartTime", ascTimeNow )
        entry = entry.replace("$$$PkgDuration", str(duration) )

        self._tempFile4SummaryReportBody.write( entry )

        

    def addTestCaseEntry ( self, className, TestCaseName, EntryType, text ):
        """
            EntryType can be: Pass, Warning, Failure, Error, Log, Attach
        """
        # Check if className is a new one
        if self._lastTestClassProcessed != className :
            if self._tempFile4ClassReportBody != None :
                self._closeTestClassReport( )
            # Lets create a new ClassReportBody file
            self._tempFile4ClassReportBody = file(self._BodyFileName_Class, "wb" )
            self._classNumTests = 0
            self._classNumWarnings = 0
            self._classNumFailures = 0
            self._classNumErrors = 0
            self._lastTestClassProcessed = className

        entry = TestClass_page_entry
        entry = entry.replace("$$$EntryType", EntryType)
        entry = entry.replace("$$$TestCaseName", className + "." + TestCaseName)
        entry = entry.replace("$$$EntryType", EntryType)
        entry = entry.replace("$$$Description", text)

        if EntryType == "Pass":
            self._totalNumTests += 1
            self._classNumTests += 1

        if EntryType == "Warning":
            self._totalNumTests += 1
            self._classNumTests += 1
            self._totalNumWarnings += 1
            self._classNumWarnings += 1
            self._tempFile4WarningOnlyReportBody.write(entry)
            
        if EntryType == "Failure":
            self._totalNumTests += 1
            self._classNumTests += 1
            self._totalNumFailures += 1
            self._classNumFailures += 1
            self._tempFile4FailureOnlyReportBody.write(entry)

        if EntryType == "Error":
            self._totalNumTests += 1
            self._classNumTests += 1
            self._totalNumErrors += 1
            self._classNumErrors += 1
            self._tempFile4ErrorOnlyReportBody.write(entry)
            
        self._tempFile4AllTestsReportBody.write(entry)
        entry = entry.replace("$$$TestCaseName", TestCaseName)
        self._tempFile4ClassReportBody.write(entry)

    def close(self):
        if self._tempFile4ClassReportBody != None :
            self._closeTestClassReport( )

        self._closeSummaryPage()
        self._closeAllTestsPage()
        self._closeWarningsOnlyPage()
        self._closeFailuresOnlyPage()
        self._closeErrorsOnlyPage()
        self._tempFile4FailureOnlyReportBody.close()
        self._tempFile4ErrorOnlyReportBody.close()
        #self._tempFile4SummaryReportBody.close()

    def deployReports ( self ):
        # deploy to http server
        if self._testConfig["deployHtmlReports"] != 0:
            shutil.copytree ( self._htmlDir, self._testConfig["deployHtmlReportsDir"] + "/" + self._testConfig["testID"] )

        # lets send notification
        if self._testConfig["sendEmail"] != 0:

            print "Send Emails"

            filename = self._testConfig["TestDir"] + "/emaillist.txt"
            f = file(filename)
            toList = []
            while 1:
                l = f.readline()
                if l == "": break
                if len(l) < 2: continue
                if l[0] == '#': continue
                l = l.split()
                toList.append(l[0])
            f.close()
    
            print "destination = ", toList

            fromaddr = 'm@varanda.ca'  
            server = 'SMPT.WHATEVER.com' 
            username = 'varanda'  
            password = 'xxxxxxx'

            subject = "Unit Test: " + self._testConfig["TestName"] + " ID: " + self._testConfig["testID"]
            body = "Automatic generated message:\n\nResults for " + subject + " are avalible at the following link:\n\n"
            body += "http://127.0.0.1/" + self._testConfig["testID"] + "/Summary.html\n\n"

            emailsender.emailsender( username, password, toList, fromaddr, subject, body, server )
            print "Email body:"
            print body
            print "Emails were sent\n"


summary_page__top = """
<html xmlns:lxslt="http://xml.apache.org/xslt" xmlns:stringutils="xalan://org.apache.tools.ant.util.StringUtils"><head>
<meta http-equiv="Content-Type" content="text/html; charset=us-ascii">
<title>Unit Test Results: Summary</title>
<link rel="stylesheet" type="text/css" title="Style" href="../stylesheet.css">
<a href="http://www.varanda.ca"><img src="../logo.png" style="border-style: none" width="271" height="29" alt="Company logo"  /></a>
<center><h1>Unit Test Results for: $$$TestName</h1></center>
<center><h2>$$$DateAndTime</h2></center>
<center><h1>Summary</h1></center>
<table width="100%">
<tbody><tr>
</tr>
</tbody></table>
<hr size="1">
<h2>Overall Summary</h2>
<table class="details" width="95%" border="0" cellpadding="5" cellspacing="2">
<tbody><tr valign="top">
<th>Tests</th><th>Warnings</th><th>Failures</th><th>Errors</th><th>Success rate</th><th nowrap="nowrap">Start Time</th><th nowrap="nowrap">Duration</th>
</tr>
<tr class="Error" valign="top">
<td><a title="Display all tests" href="$$$LinkToAllTests">$$$TotalNumTests</a></td>
<td><a title="Display all warnings" href="$$$LinkToAllWarnings">$$$TotalNumWarnings</a></td>
<td><a title="Display all failures" href="$$$LinkToAllFailures">$$$TotalNumFaillures</a></td>
<td><a title="Display all errors" href="$$$LinkToAllErrors">$$$TotalNumErrors</a></td>
<td>$$$SuccessRate %</td>
<td>$$$StartTime</td>
<td>$$$Duration</td>
</tr>
</tbody></table>
<table width="95%" border="0">
<tbody><tr>
<td style="text-align: justify;">
Note: <bold>failures </bold>  are problems with device under test <bold>errors </bold> are buggy test-cases.
</td></tr></tbody></table>
<h2>Test case Classes:</h2>
<table class="details" width="95%" border="0" cellpadding="5" cellspacing="2">
<tbody><tr valign="top">
<th width="80%">Name</th><th>Tests</th><th>Warnings</th><th>Failures</th><th>Errors</th><th nowrap="nowrap">Start Time</th><th nowrap="nowrap">Duration</th>
</tr>
"""

summary_page__entry = """
<!-- $$$EntryType can be: Pass, Failure, Error (Log) -->
<tr class="$$$EntryType" valign="top">
<td><a href="$$$LinkToTestClass">$$$TestClassName</a></td
><td>$$$PkgNumTests</td>
<td>$$$PkgNumWarnings</td>
<td>$$$PkgNumFailures</td>
<td>$$$PkgNumErrors</td>
<td>$$$PkgStartTime</td>
<td>$$$PkgDuration</td>
</tr>
"""

summary_page__botton = """
</tbody></table>
</body></html>
"""

TestClass_page_top = """
<html xmlns:lxslt="http://xml.apache.org/xslt" xmlns:stringutils="xalan://org.apache.tools.ant.util.StringUtils"><head>
<meta http-equiv="Content-Type" content="text/html; charset=us-ascii">
<title>Unit Test Results: Test Class</title>
<link rel="stylesheet" type="text/css" title="Style" href="../stylesheet.css">
<a href="http://www.varanda.ca"><img src="../logo.png" style="border-style: none" width="271" height="29" alt="Company logo"  /></a>
<center><h1>Unit Test Results for $$$TestClassName class</h1></center>
<center><h2>$$$DateAndTime</h2></center>
<a title="Go to Summary Page" href="Summary.html">Home</a>
<table width="100%">
<tbody><tr></tr></tbody></table>
<hr size="1">
<h2>Summary</h2>
<table class="details" width="95%" border="0" cellpadding="5" cellspacing="2">
<tbody><tr valign="top">
<th>Tests</th><th>Warnings</th><th>Failures</th><th>Errors</th><th>Success rate</th><th nowrap="nowrap">Start Time</th><th nowrap="nowrap">Duration</th>
</tr>
<tr class="Error" valign="top">
<td>$$$NumTests</td>
<td>$$$NumWarnings</td>
<td>$$$NumFaillures</td>
<td>$$$NumErrors</td>
<td>$$$SuccessRate %</td>
<td>$$$StartTime</td>
<td>$$$Duration</td>
</tr>
</tbody></table>
<table width="95%" border="0">
<tbody><tr>
<td style="text-align: justify;">
Note: <bold>failures </bold>  are problems with device under test <bold>errors </bold> are buggy test-cases.
</td>
</tr>
</tbody></table>
<h2>Test case Logs for $$$TestClassName class:</h2>
<table class="details" width="95%" border="0" cellpadding="5" cellspacing="2">
<tbody><tr valign="top">
<th width="20%">TestCase</th><th width="5%">Result</th><th>Description</th>
</tr>
"""

TestClass_page_entry = """
<!-- $$$EntryType can be: Pass, Failure, Error (Log) -->
<tr class="$$$EntryType" valign="top">
<td> $$$TestCaseName</td>
<td>$$$EntryType</td>
<td>$$$Description</td>
"""

TestClass_page_botton = """
</tbody></table>
</body></html>
"""

individual_page__top = """
<html xmlns:lxslt="http://xml.apache.org/xslt" xmlns:stringutils="xalan://org.apache.tools.ant.util.StringUtils"><head>
<meta http-equiv="Content-Type" content="text/html; charset=us-ascii">
<title>Unit Test Results: $$$TestName</title>
<link rel="stylesheet" type="text/css" title="Style" href="../stylesheet.css">
<a href="http://www.varanda.ca"><img src="../logo.png" style="border-style: none" width="271" height="29" alt="Company logo"  /></a>
<center><h1>Unit Test Results -  $$$TestName</h1></center>
<center><h1>$$$ReportType</h1></center>
<center><h2>$$$DateAndTime</h2></center>
<a title="Go to Summary Page" href="Summary.html">Home</a>
<table width="100%">
<tbody><tr>
</tr>
</tbody></table>
<hr size="1">
<h2>Overall Summary</h2>
<table class="details" width="95%" border="0" cellpadding="5" cellspacing="2">
<tbody><tr valign="top">
<th>Tests</th><th>Warnings</th><th>Failures</th><th>Errors</th><th>Success rate</th><th nowrap="nowrap">Start Time</th><th nowrap="nowrap">Duration</th>
</tr>
<tr class="Error" valign="top">
<td><a title="Display all tests" href="$$$LinkToAllTests">$$$TotalNumTests</a></td>
<td><a title="Display all warnings" href="$$$LinkToAllWarnings">$$$TotalNumWarnings</a></td>
<td><a title="Display all failures" href="$$$LinkToAllFailures">$$$TotalNumFaillures</a></td>
<td><a title="Display all errors" href="$$$LinkToAllErrors">$$$TotalNumErrors</a></td>
<td>$$$SuccessRate %</td>
<td>$$$StartTime</td>
<td>$$$Duration</td>
</tr>
</tbody></table>
<h2>$$$ReportType Log:</h2>
<table class="details" width="95%" border="0" cellpadding="5" cellspacing="2">
<tbody><tr valign="top">
<th width="20%">TestCase</th><th width="5%">Result</th><th>Description</th>
</tr>
"""


    

