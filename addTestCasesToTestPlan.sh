#!/bin/bash -exu

# Name: Get TCs data via TestLink-API-Python
# Version: 1.0
# Author: Valentina Dokova

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# The script requires the following packages:
# # testlink
# # python 2.7
# # wget

# Set TestLink server URL
export TESTLINK_API_PYTHON_SERVER_URL=http://10.243.64.7/testlink/lib/api/xmlrpc/v1/xmlrpc.php

# Define your personal TestLink API Devkey
printf "Please, input your testlink devkey\nIt can be found in TestLink -> My Settings -> Personal API access key:\n"
read testlinkDevkey
export TESTLINK_API_PYTHON_DEVKEY=$testlinkDevkey

python ./addTestCasesToTestPlan.py
