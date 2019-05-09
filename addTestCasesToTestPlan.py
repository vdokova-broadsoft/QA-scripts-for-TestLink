# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Name: Get TCs data and manage Test Plans via TestLink-API-Python
# Version: 1.1
# Author: Valentina Dokova
#
# Should previously set TestLink server URL and generated personal API DevKey
# # export TESTLINK_API_PYTHON_SERVER_URL=http://10.243.64.7/testlink/lib/api/xmlrpc/v1/xmlrpc.php
# # export TESTLINK_API_PYTHON_DEVKEY='It can be found in TestLink -> My Settings -> Personal API access key'
#
# TestLink-API-Python-client 0.8.0
# https://pypi.org/project/TestLink-API-Python-client/
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ----------------------------- Imports ---------------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import testlink
from testlink import TestlinkAPIClient, TestLinkHelper, TestGenReporter
from testlink.testlinkerrors import TLResponseError
import xml.etree.ElementTree as ElemTree
import wget
import ssl
import os

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ------------------------ Connect TestLink -----------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
tls = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ----------------------- Define global constants -----------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
testProject = 'Iris'
testCasePrefix = 'IRIS'

currentTestProjectID = tls.getProjectIDByName(testProject)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# --------------------------- Define functions --------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Function for getting the Test Plan ID when input Test Project name and Test Plan name.
def getTestPlanID (testProject, testPlan):
    return int(tls.getTestPlanByName(testProject, testPlan)[0]['id'])

# Function for downloading _output-XX file from the Jenkins
def downloadAllTCsFromJenkins (allTestCases):
    while not (allTestCases):
        # Download the file for all test cases from the Jenkins _output-XX.xml
        buildJob = raw_input('Please, input the link for the desired Jenkins job.\nExample: https://ci.sof.broadsoft.com/view/TA/job/ui-test-connect-android-full-stable-3-7-x/: ')
        buildNumber = raw_input('Please, input the the desired build number.\nExample: 19: ')
        allTestCasesURL = buildJob + buildNumber + '/robot/report/_output-' + buildNumber +'.xml'

        # Create a folder and specify the name for the downloaded file
        resourcesDir = 'resources'
        allTCsFile = resourcesDir + '/allTCs.xml'

        if (os.path.isdir(resourcesDir)):
            if (os.path.isfile(allTCsFile)):
                os.remove(allTCsFile)
        else:
            os.mkdir(resourcesDir)

        # Download the file
        ssl._create_default_https_context = ssl._create_unverified_context

        try:
            allTestCases = wget.download(allTestCasesURL, allTCsFile)
        except:
            print ('\n')
            print ('Something went wrong during the downloading. Please, input again the URL and Jenkins Job Build number.\n')

    print ('\n')
    
    # Return the file
    return allTestCases

# Function for downloading _test_link_results-XX file from the Jenkins
def downloadPassedTCsFromJenkins (passedTestCases):   
    while not (passedTestCases):
        # Download the file for the passed test cases from the Jenkins _test_link_results-XX.xml
        buildJob = raw_input('Please, input the link for the desired Jenkins job.\nExample: https://ci.sof.broadsoft.com/view/TA/job/ui-test-connect-android-full-stable-3-7-x/: ')
        buildNumber = raw_input('Please, input the the desired build number.\nExample: 19: ')
        passedTestCasesURL = buildJob + buildNumber + '/robot/report/_test_link_results-' + buildNumber +'.xml'
        
        # Create a folder and specify the name for the downloaded file
        resourcesDir = 'resources'
        passedTCsFile = resourcesDir + '/passedTCs.xml'

        if (os.path.isdir(resourcesDir)):
            if (os.path.isfile(passedTCsFile)):
                os.remove(passedTCsFile)
        else:
            os.mkdir(resourcesDir)
        
        # Download the file
        ssl._create_default_https_context = ssl._create_unverified_context

        try:
            passedTestCases = wget.download(passedTestCasesURL, passedTCsFile)
        except:
            print ('\n')
            print ('Something went wrong during the downloading. Please, input again the URL and Jenkins Job Build number.\n')
    
    print ('\n')

    # Return the file
    return passedTestCases

# Function for input Test Plan name until the input is an existing Test Plan. 
def inputExistingTestPlan (testPlan):
    testPlanInfo = 0
    while not (testPlanInfo):
        testPlan = raw_input('Please, input the name of the Test Plan: ')

        try:
            testPlanInfo = tls.getTestPlanByName (testProject, testPlan)
        except TLResponseError:
            print ('This Test Plan doesn\'t exist. Please, input again the name of the test plan.\n')

    return testPlan

# Function for input Test Plan name until the input is an non-existing Test Plan. 
def inputNonExistingTestPlan (testPlan):
    while True:
        testPlan = raw_input('Please, input a name for the Test Plan: ')

        try:
            tls.getTestPlanByName (testProject, testPlan)
            print ('This Test Plan already exists! Please, input a new name.\n')
        except TLResponseError:
            tls.createTestPlan(testPlan, testProject)
            print ('Created ' + testProject + ' -> ' + testPlan)
            break

    return testPlan

# Function to parse downloaded file for all test cases - _output-XX.xml and add test cases' ids to a list.
def getExternalIds(allTestCases):
    externalIDs = []
    tree = ElemTree.parse(allTestCases)
    root = tree.getroot()
    for n in range(len(root[0])):
        testCases = root[0][n].findall('test')
        for k in range(len(testCases)):
            testCaseName = testCases[k].get('name')
            testCaseID = testCaseName.split(':')
            testCaseExtID = (testCasePrefix + '-' + str(testCaseID[0]))
            externalIDs.append(testCaseExtID)
    
    return externalIDs

# Function for input keyword until the input is an existing keyword. 
def inputExistingKeyword (keyword):
    keywordInfo = 0
    while not (keywordInfo):
        keyword = raw_input('Please, input the keyword: ')

        # Create a dict with all keywords from the project
        keywords = tls.getProjectKeywords(tls.getProjectIDByName(testProject))

        # Check if the keyword exists in this project
        keywordInfo = keyword in keywords.values()

        if (keywordInfo == False):
            print ('This Keyword doesn\'t exist. Please, input again the keyword.\n')

    return keyword

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ------------------------------ Code -----------------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Ask the user to select what he wants to do 
while True:
    print ('\n')
    print ('Please, input what you want to do:\n 1: Create new test plan from all TCs from a Jenkins job.\n 2: Create new test plan from passed TCs from a Jenkins job.\n 3: Add all TCs from a Jenkins job to an existing test plan.\n 4: Add passed TCs from a Jenkins job to an existing test plan.\n 5: Add all TCs from an existing test plan to another.\n 6: Add an existing keyword to all TCs from an existing test plan.')
    switcher = raw_input('Your choice: ')
    print ('\n')

    # Option 1: Create new test plan from all TCs from a Jenkins job
    if switcher == '1':

        print ('You have selected: Create new test plan from all TCs from a Jenkins job.\n')
        
        # Download all test cases from a Jenkins job
        allTestCases = ''
        allTestCases = downloadAllTCsFromJenkins(allTestCases)

        # Ask the user to input name for the Test Plan. It should not exist.
        testPlan = ''
        testPlan = inputNonExistingTestPlan(testPlan)
        
        # Parse the downloaded file and add test cases' ids to a list
        externalIDs = getExternalIds(allTestCases)

        # Add test cases to the test plan
        currentTestPlanID = getTestPlanID(testProject, testPlan)
        testCasesCount = len(externalIDs)

        for n in range(testCasesCount):
            tcExternalID = externalIDs[n]
            tcVersion = int(tls.getTestCase(testcaseexternalid=tcExternalID)[0]['version'])
            tls.addTestCaseToTestPlan(testprojectid=currentTestProjectID, testplanid=currentTestPlanID, testcaseexternalid=tcExternalID, version=tcVersion)
            print('Processed ' + str(n+1) + '/' + str(testCasesCount))

        print('\nDone.\nCreated ' + str(testPlan) + ' test plan from all test cases from the Jenkins job.\nHave a successful and smiley day! :))\n')
        break

    # Option 2: Create new test plan from passed TCs from a Jenkins job
    elif switcher == '2':

        print ('You have selected: Create new test plan from passed TCs from a Jenkins job.\n')
        
        # Download passed test cases from a Jenkins job
        passedTestCases = ''
        passedTestCases = downloadPassedTCsFromJenkins(passedTestCases)

        # Ask the user to input name for the Test Plan. It should not exist.
        testPlan = ''
        testPlan = inputNonExistingTestPlan(testPlan)

        # Parse the downloaded file and find all test cases
        tree = ElemTree.parse(passedTestCases)
        root = tree.getroot()
        testCases = root.findall('testcase')

        # Add test cases to the test plan
        currentTestPlanID = getTestPlanID(testProject, testPlan)
        testCasesCount = len(testCases)

        for n in range (testCasesCount):
            tcExternalID = testCases[n].get('external_id')
            tcVersion = int(tls.getTestCase(testcaseexternalid=tcExternalID)[0]['version'])
            tls.addTestCaseToTestPlan(testprojectid=currentTestProjectID, testplanid=currentTestPlanID, testcaseexternalid=tcExternalID, version=tcVersion)
            print('Processed ' + str(n+1) + '/' + str(testCasesCount))

        print('\nDone.\nCreated ' + str(testPlan) + ' test plan from passed test cases from the Jenkins job.\nHave a successful and smiley day! :))\n')
        break
    
    # Option 3: Add all TCs from a Jenkins job to an existing test plan
    elif switcher == '3':

        print ('You have selected: Add all TCs from a Jenkins job to an existing test plan.\n')
        
        # Download all test cases from a Jenkins job
        allTestCases = ''
        allTestCases = downloadAllTCsFromJenkins(allTestCases)
        
        # Ask the user to input name of the Test Plan. It should already exist.
        testPlan = ''
        testPlan = inputExistingTestPlan(testPlan)
        
        # Parse the downloaded file and add test cases' ids to a list
        externalIDs = getExternalIds(allTestCases)

        # Add test cases to the test plan
        currentTestPlanID = getTestPlanID(testProject, testPlan)
        testCasesCount = len(externalIDs)

        for n in range(testCasesCount):
            tcExternalID = externalIDs[n]
            tcVersion = int(tls.getTestCase(testcaseexternalid=tcExternalID)[0]['version'])
            tls.addTestCaseToTestPlan(testprojectid=currentTestProjectID, testplanid=currentTestPlanID, testcaseexternalid=tcExternalID, version=tcVersion)
            print('Processed ' + str(n+1) + '/' + str(testCasesCount))

        print('\nDone.\nAdded all test cases from the Jenkins job to ' + str(testPlan) + ' test plan.\nHave a successful and smiley day! :))\n')
        break
    
    # Option 4: Add passed TCs from a Jenkins job to an existing test plan
    elif switcher == '4':

        print ('You have selected: Add passed TCs from a Jenkins job to an existing test plan.\n')
        
        # Download passed test cases from a Jenkins job
        passedTestCases = ''
        passedTestCases = downloadPassedTCsFromJenkins(passedTestCases)

        # Ask the user to input name of the Test Plan. It should already exist.    
        testPlan = ''
        testPlan = inputExistingTestPlan(testPlan)

        # Parse the downloaded file and find all test cases
        tree = ElemTree.parse(passedTestCases)
        root = tree.getroot()
        testCases = root.findall('testcase')

        # Add test cases to the test plan
        currentTestPlanID = getTestPlanID(testProject, testPlan)
        testCasesCount = len(testCases)

        for n in range (testCasesCount):
            tcExternalID = testCases[n].get('external_id')
            tcVersion = int(tls.getTestCase(testcaseexternalid=tcExternalID)[0]['version'])
            tls.addTestCaseToTestPlan(testprojectid=currentTestProjectID, testplanid=currentTestPlanID, testcaseexternalid=tcExternalID, version=tcVersion)
            print('Processed ' + str(n+1) + '/' + str(testCasesCount))

        print('\nDone.\nAdded passed test cases from the Jenkins job to ' + str(testPlan) + ' test plan.\nHave a successful and smiley day! :))\n')
        break

    # Option 5: Add all TCs from an existing test plan to another
    elif switcher == '5':

        print ('You have selected: Add all TCs from an existing test plan to another.\n')

        # Ask the user to input names of the Test Plans. Both of them should already exist.
        print ('Test Plan from which you want to export.')
        testPlanFrom = ''
        testPlanFrom = inputExistingTestPlan(testPlanFrom)

        print ('Test Plan to which you want to import.')
        testPlanTo = ''
        testPlanTo = inputExistingTestPlan(testPlanTo)

        # Add test cases from first to the second test plan
        testPlanFromID = getTestPlanID(testProject, testPlanFrom)
        testPlanToID = getTestPlanID(testProject, testPlanTo)

        testsForImport = tls.getTestCasesForTestPlan(testPlanFromID)
        testsForImportCount = len(testsForImport)

        for n in range (testsForImportCount):
            tcExternalID = testsForImport.values()[n][0]['full_external_id']
            tcVersion = int(tls.getTestCase(testcaseexternalid=tcExternalID)[0]['version'])
            tls.addTestCaseToTestPlan(testprojectid=currentTestProjectID, testplanid=testPlanToID, testcaseexternalid=tcExternalID, version=tcVersion)
            print('Processed ' + str(n+1) + '/' + str(testsForImportCount))

        print('\nDone.\nAdded all test cases from ' + str(testPlanFrom) + ' test plan to ' + str(testPlanTo) + ' test plan.\nHave a successful and smiley day! :))\n')
        break

    # Option 6: Add an existing keyword to all TCs from an existing test plan
    elif switcher == '6':

        print ('You have selected: Add an existing keyword to all TCs from an existing test plan.\n')

        # Ask the user to input the name of the Test Plan. It should already exist.
        testPlan = ''
        testPlan = inputExistingTestPlan(testPlan)

        # Ask the user to input the keyword. It should already exist.
        keyword = ''
        keyword = inputExistingKeyword(keyword)

        # Add the keyword to all test cases from the selected test plan
        currentTestPlanID = getTestPlanID(testProject, testPlan)

        testsForKeywords = tls.getTestCasesForTestPlan(currentTestPlanID)
        testsForKeywordsCount = len(testsForKeywords)

        for n in range (testsForKeywordsCount):
            tcExternalID = testsForKeywords.values()[n][0]['full_external_id']
            tls.addTestCaseKeywords({tcExternalID : [keyword]})
            print('Processed ' + str(n+1) + '/' + str(testsForKeywordsCount))

        print('\nDone.\nAdded keyword ' + str(keyword) + ' to all test cases from ' + str(testPlan) + ' test plan.\nHave a successful and smiley day! :))\n')
        break

    # If the user inputs an incorrect value, return to the input screen.
    else:
        print ('Incorrect input! Please, input a number from 1 to 6.')
