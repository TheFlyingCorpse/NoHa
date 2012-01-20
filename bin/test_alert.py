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
import ruleeval

def usage():
	print(sys.argv[0] + " - Forward notifcations to NoHa")
	print("")
	print("Valid options are:")
	print("  -h, --help            Prints this message")
	print("  -a, --application     Application name, ex: icinga")
        print("  -I, --instance        Instance of application (optional)")
        print("  -i, --input           Input to parse on to NoHa for filtering")
        print("  -p, --pipe            Full path to pipe (not implemented)")
        print("  -s, --socket          Adress to socket (not implemented)")

def alert(application,instance, input, verbose):
	if verbose:
		print("Application: " + application)
		print("Instance:    " + instance)
		print("Input:       " + input)


def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ha:Ii:v", ["help", "application=", "instance=", "input="])
	except getopt.GetoptError, err:
		#print help information and exit:
		print(str(err))
		usage()
		sys.exit(2)

	# Set defaults
	application = None
	instance = None
	input = None
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
		else:
			assert False, "unhandled option"

	# Call alert function to pass on the information
	alert(str(application), str(instance), str(input), verbose)

if __name__ == "__main__":
	main()
