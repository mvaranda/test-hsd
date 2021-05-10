import os, sys, imp, time, unittest, demo_unittest


def readTestConfig(testDir):
    """
        This function reads the file config.txt.
    """

    filename = testDir + "/config.txt"
    f = file(filename)
    cfg = {}
    while 1:
        l = f.readline()
        if l == "": break
        l = l.replace(" ",'')
        if l[0] == '#': continue
        l = l.split("=")
        if len(l) == 0: continue
        if len(l[0]) < 2: continue
        #if l[1] != "=": continue
        l[1] = l[1].replace("\r",'')
        l[1] = l[1].replace("\n",'')

        if l[0] == 'http_dir':
            cfg["http_dir"] = l[1]

        if l[0] == 'TestName':
            cfg["TestName"] = l[1]

        if l[0] == 'deployHtmlReports':
            if l[1].lower() == 'yes':
                cfg['deployHtmlReports'] = 1
            else:
                cfg['deployHtmlReports'] = 0

        if l[0] == 'deployHtmlReportsDir':
            cfg["deployHtmlReportsDir"] = l[1]

        if l[0] == 'sendEmail':
            if l[1].lower() == 'yes':
                cfg['sendEmail'] = 1
            else:
                cfg['sendEmail'] = 0

    f.close()
    if 1:
        print "Config:"
        print "    http_dir: ", cfg["http_dir"]
        print "    TestName: ", cfg["TestName"]
        print "    deployHtmlReports: ", cfg['deployHtmlReports']
        print "    deployHtmlReportsDir: ", cfg["deployHtmlReportsDir"]
        print "    sendEmail: ", cfg['sendEmail']
    return cfg

def readTestFilenames(testDir):
    """
        This function reads the file testlist.txt under the
        provided directory. It returns a list of filenames read
        from that file filtering out the newline and comments.
    """

    filename = testDir + "/testlist.txt"
    f = file(filename)
    files = []
    while 1:
        l = f.readline()
        if l == "": break
        if l[0] != '#':
            l = l.split()
            if len(l) == 0: continue
            if len(l[0]) > 1:
                files.append(testDir + "/" + l[0])
    f.close()
    return files

def runAllTestFiles (TestFilenameList, testConfig):
    rootTestName = testConfig["TestName"]
    i = 1
    suite = unittest.TestSuite()
    for filename in TestFilenameList:
        print "...",filename
        moduleToTest = imp.load_source(rootTestName + "_" + i.__str__(), filename, file(filename))
        suite.addTest(unittest.TestLoader().loadTestsFromModule(moduleToTest))
        i = i + 1
    demo_unittest.DemoTestRunner(testConfig).run(suite)

def mergeFiles( fileA, fileB, mergedFile ):
    fout = file(mergedFile,'wb')
    for n in [fileA,fileB]:
        fin  = file(n,'rb')
        while True:
            data = fin.read(16384) # read in blocks of 16K
            if not data: break
            fout.write(data)
        fin.close()
    fout.close()


if __name__ == '__main__':
    try:
        testDir = os.path.abspath('') + "/" + sys.argv[1]
    except:
        print "test dir not provided... assume DEMO"
        testDir = os.path.abspath('') + "/DEMO"
    print "dir = ",testDir

    sys.path.append(os.path.abspath(''))
    sys.path.append(testDir)

    testConfig = readTestConfig(testDir)
    testID = testConfig["TestName"] + "_" + str(time.time())
    testID = testID.replace(".","_")
    testConfig["testID"] = testID
    testConfig["TestDir"] = testDir
    print "config = \n    ",testConfig
    listToRun = readTestFilenames(testDir)
    print "\n\nTest files to run:\n"
    runAllTestFiles(listToRun, testConfig)

