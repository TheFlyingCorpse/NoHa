#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        test1
# Purpose:     Test1 of NoHa, to verify filters are properly processed
#
# Author:      Rune "TheFlyingCorpse" Darrud
#
# Created:     19.01.2012
# Copyright:   (c) Rune "TheFlyingCorpse" Darrud 2012
# Licence:     GPL 2
#-------------------------------------------------------------------------------

# Import sys class
import sys

# Import classes from the lib folder
sys.path.append('../lib/')
sys.path.append('lib/')

from ruleeval import ruleeval

# make it easier to read
r = ruleeval()



input = "HOSTGROUPS=linuxsrv,linux-apache;SERVICEGROUPS=apache-svc,tomcat-svc,mysql;_AGENT_NRPE=YES;HOST=websrv32;SERVICE=Apache;_CRITICALITY=PRODUCTION"

condition_list = [
    'HOSTGROUPS;&;linux-mysql',
    'HOSTGROUPS;!;linux-apache',
    'SERVICEGROUPS;&;apache-svc',
    '_CRITICALITY;&;PRODUCTION',
    '_AGENT_NSCP;!;NO',
    ]


result = r.evaluate_input_vs_conditions(input,";",condition_list,";")
if result:
    print("FALSE, RULES MATCH")
else:
    print("OK, CONDITIONS DOES NOT MATCH")
