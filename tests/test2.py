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



input = "HOSTGROUPS=windows-servers,mssql-srv,exchange-srv;SERVICEGROUPS=mssqlsvc,exchange-svc;_AGENT_NSCP=YES;HOST=exchange22;SERVICE=Memory"

condition_list = [
    'HOSTGROUPS;!;lab*,dev*',
    'HOSTGROUPS;&;windows-servers,exchange-srv',
    'SERVICEGROUPS;&;exchange-svc',
    '_AGENT_NSCP;&;YES',
    ]


result = r.evaluate_input_vs_conditions(input,";",condition_list,";")
if result:
    print("OK, RULES MATCH")
else:
    print("FALSE, CONDITIONS DOES NOT MATCH")
