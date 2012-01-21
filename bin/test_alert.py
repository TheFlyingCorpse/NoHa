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

def alert(debug, verbose, application,instance, input, input_delimiter, input_separator):
	if verbose:
		print("Passing the following arguments on:")
		if application:			print("Application:       " + application)
		if instance:			print("Instance:          " + instance)
		if input:				print("Input:             " + input)
		if input_delimiter:		print("Input delimiter:   " + input_delimiter)
		if input_separator: 	print("Input separator:   " + input_separator)
		if verbose:             print("Verbose:           " + str(verbose))
		if debug:				print("Debug:             " + str(debug))
		print("")

	test_result = r.eval_input_of_application(debug,verbose,application,instance,input,input_delimiter,input_separator)
	if verbose:
		print("")
		print("Test Result:")
		if test_result:
			print("Alert OK, matching rule")
		elif not test_result:
			print("Alert OK, no matching rule")
		else:
			print("Alert result unknown")

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
	alert(debug, verbose, str(application), instance, str(input), delimiter, separator)

if __name__ == "__main__":
	main()
