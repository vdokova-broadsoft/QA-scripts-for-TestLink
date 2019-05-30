# QA-scripts-for-TestLink
QA scipts based on TestLink-API-Python-client - https://pypi.org/project/TestLink-API-Python-client/.

# Introduction

These scripts are based on TestLink-API-Python-client.

TestLink-API-Python-client is a Python XML-RPC client for TestLink_.

Initially based on James Stock testlink-api-python-client R7 and  Olivier 
Renault JinFeng_ idea - an interaction of TestLink_, `Robot Framework`_ and Jenkins_.

# Preconditions

You should install following packages from Bash terminal (You can use Cigwin on Windows):
- python 2.7
- testlink:
```
pip install TestLink-API-Python-client
```
- wget:
```
brew install wget
```
(If there is an error that wget cannot be imported use:
```
pip install wget
```
This will install the propper version of wget for python 2.)

# How to run the script

Currently there are two script files in this repo - python and bash.
Download them and put in a folder (during the script files will be downloaded in sub-folder named resources)
To start the you should open a bash terminal, open the folder with the scripts and and simply run it:
```
./addTestCasesToTestPlan.sh
```
And that's it - you are ready to use it!

# What does it do

You will be able to choose from the following operations:

1. Create new test plan from all TCs from a Jenkins job.
2. Create new test plan from passed TCs from a Jenkins job.
3. Add all TCs from a Jenkins job to an existing test plan.
4. Add passed TCs from a Jenkins job to an existing test plan.
5. Add all TCs from an existing test plan to another.
6. Add an existing keyword to all TCs from an existing test plan.

If there are any questions - don't hesitate to contact me. :))
