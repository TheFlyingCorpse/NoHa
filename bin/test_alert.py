#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        test_alert.py
# Purpose:     Simple script that sets in motion sending of alerts via NoHa
#
# Author:      Rune "TheFlyingCorpse" Darrud
#
# Created:     20.01.2012
# Copyright:   (c) Rune "TheFlyingCorpse" Darrud 2012
# Licence:     GPL 2
#-------------------------------------------------------------------------------

import sys, getopt
sys.path.append('../lib/')
sys.path.append('lib/')
from ruleeval import ruleeval

# Make it shorter
r = ruleeval()

def usage():
	print(sys.argv[0] + " - Forward notifcations to NoHa")
	print("")
	print("Valid options are:")
	print("  -h, --help            Prints this message")
#	print("                        Optional arguments: nagios ")
	print("")
	print("  -a, --application     Application name, ex: icinga, nagios, centreon or shinken")
	print("  -I, --instance        Instance of application (optional)")
	print("  -i, --input           Input to parse on to NoHa for filtering")
	print("  -d, --delimiter       Delimiter between name=value and name=value, ex ; (optional)")
	print("  -s, --separator       Separator between name=value and value, ex , (optional)")
	print("  -p, --pipe            Full path to pipe (not implemented)")
	print("  -S, --socket          Adress to socket (not implemented)")

def usage_nagios():
	print("  ")

def alert(application,instance, input, input_delimiter, input_separator, verbose):
	if verbose:
		print("Passing the following arguments on:")
		print("Application:       " + application)
		print("Instance:          " + instance)
		print("Input:             " + input)
		print("Input delimiter:   " + input_delimiter)
		print("Input separator:   " + input_separator)
		print("")

	alert_result = r.eval_input_of_application(application,instance,input,input_delimiter,input_separator)
	if verbose:
		print("Result:")
		if alert_result:
			print("Alert OK, matching rule")
		elif not alert_result:
			print("Alert OK, no matching rule")
		else:
			print("Alert result unknown")

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ha:Ii:vd:s:", ["help", "application=", "instance=", "input=", "delimiter=", "separator="])
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

	# Loop through all arguments
	for o, a in opts:
		if o == "-v":
			verbose = True
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
	alert(str(application), str(instance), str(input), str(delimiter), str(separator), verbose)

if __name__ == "__main__":
	main()
