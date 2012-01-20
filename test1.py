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

# Import classes
from ruleeval import ruleeval

# make it easier to read
r = ruleeval()



input = "HOSTGROUPS=linuxsrv,linux-mysql,linux-postfix;SERVICEGROUPS=mysql-svc,mysql;_AGENT_NRPE=YES;HOST=mailsrv03;SERVICE=MySQL"

condition_list = [
    'HOST;&;mailsrv*',
    'HOST;!;windows',
    'HOSTGROUPS;!;edir,oes2',
    'HOSTGROUPS;&;linux-*,linux-postfix',
    'SERVICEGROUPS;&;mysql-svc,ssh-srv',
    '_AGENT_NRPE;&;YES',
    ]


result = r.evaluate_input_vs_conditions(input,";",condition_list,";")
if result:
    print("OK, RULES MATCH")
else:
    print("FALSE, CONDITIONS DOES NOT MATCH")
