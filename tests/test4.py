#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        test4.py
# Purpose:     Test the interface classes for their functionality
#
# Author:      Rune "TheFlyingCorpse" Darrud
#
# Created:     21.01.2012
# Copyright:   (c) Rune "TheFlyingCorpse" Darrud 2012
# Licence:     GPL 2
#-------------------------------------------------------------------------------

import sys, getopt
sys.path.append('../lib/')
sys.path.append('lib/')
#from ruleeval import ruleeval
from interface import interface
# Make it shorter
#r = ruleeval()
i = interface()

def usage():
	print(sys.argv[0] + " - Test4 - Interface class tests")
	print("")
	print("Valid options are:")
	print("  -h, --help            Prints this message")
	print("  -f, --config-file     config file path")
	print("")

def usage_nagios():
	print("  ")

def test(config_file, verbose):
	if verbose:
		
		print("")

	test_result, output = i.load_app_config(config_file)
	if verbose:
		print("Testresult:")
		if test_result:
			print("OK")
		elif not test_result and output:
			print(output)
		elif not test_result:
			print("Test failed")
		else:
			print("Result unknown")

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hf:v", ["help", "config-file="])
	except getopt.GetoptError, err:
		#print help information and exit:
		print(str(err))
		usage()
		sys.exit(2)

	# Set defaults
	config_file = None
	verbose = False

	# Loop through all arguments
	for o, a in opts:
		if o == "-v":
			verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-f", "--config-file"):
			config_file = a
		else:
			assert False, "unhandled option"

	# Call alert function to pass on the information
	test(str(config_file), verbose)

if __name__ == "__main__":
	main()
