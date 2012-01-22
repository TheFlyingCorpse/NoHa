#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        alert_noha.py
# Purpose:     Simple script that connects to NoHa and sends the alert
#
# Author:      Rune "TheFlyingCorpse" Darrud
#
# Created:     22.01.2012
# Copyright:   (c) Rune "TheFlyingCorpse" Darrud 2012
# Licence:     GPL 2
#-------------------------------------------------------------------------------

import sys, getopt
sys.path.append('../lib/')
sys.path.append('lib/')
#from ruleeval import ruleeval

from twisted.internet import reactor, defer
from twisted.internet.protocol import ClientCreator
from twisted.protocols import amp
from interface import SendAlert, SendData

# Make it shorter
#r = ruleeval()

def usage():
	print(sys.argv[0] + " - Forward notifcations to NoHa")
	print("")
	print("Valid options are:")
	print("  -h, --help            Prints this message")
	print("  -v                    Verbose output")
	print("  -D                    Debug output")
	print("")
	print("  -a, --application     Application name, ex: icinga, nagios, centreon or shinken")
	print("  -I, --instance        Instance of application (optional)")
	print("  -i, --input           Input to parse on to NoHa for filtering")
	print("  -d, --delimiter       Delimiter between name=value and name=value, ex ; (optional)")
	print("  -s, --separator       Separator between name=value and value, ex , (optional)")
	print("  -p, --pipe            Full path to pipe (not implemented)")
	print("  -S, --socket          Adress to socket (not implemented)")

def doAlert(debug, verbose, encryption, application, instance, input, delimiter, separator):

    ClientCreator(reactor, amp.AMP).connectTCP('127.0.0.1', 1234).addCallback(
       lambda p: p.callRemote(SendAlert, debug=debug, verbose=verbose, encryption=encryption, application=application, instance=instance, input=input, delimiter=delimiter, separator=separator)).addCallback(
           lambda result: result['result'])

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "Dvha:Ii:d:s:", ["help", "application=", "instance=", "input=", "delimiter=", "separator="])
	except getopt.GetoptError, err:
		#print help information and exit:
		print(str(err))
		usage()
		sys.exit(2)

	# Set defaults
	application = None
	instance = None
	input = None
	delimiter = None
	separator = None
	verbose = False
	debug = False
	encryption = False # not implemented

	# Loop through all arguments
	for o, a in opts:
		if o == "-v":
			verbose = True
		elif o == "-D":
			debug = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-a", "--application"):
			application = a
		elif o in ("-I", "--instance"):
			instance = a
		elif o in ("-i", "--input"):
			input = a
		elif o in ("-d", "--delimiter"):
			delimiter = a
		elif o in ("-s", "--separator"):
			separator = a
		else:
			assert False, "unhandled option"

	# Call alert function to pass on the information
	#alert(debug, verbose, str(application), instance, str(input), delimiter, separator)
	result = doAlert(debug, verbose, int(encryption), application, str(instance), input, delimiter, separator)

if __name__ == "__main__":
	#main()
	doAlert(False, False, False, 'icinga', 'None', "HOSTGROUPS=blA,blaaa;SERVICEGROUPS=hehehe", ";", ",")
	reactor.run()
	reactor.stop()
