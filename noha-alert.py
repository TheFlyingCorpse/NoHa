#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        noha-alert.py
# Purpose:     Simple script that connects to NoHa and alerts via XML-RPC
#
# Author:      Rune "TheFlyingCorpse" Darrud
#
# Created:     22.01.2012
# Copyright:   (c) Rune "TheFlyingCorpse" Darrud 2012
# Licence:     GPL 2
#-------------------------------------------------------------------------------

import sys, getopt, xmlrpclib, yaml
from interface import interface

# Make it shorter
i = interface()

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

def doAlert(YamlConfig, debug, verbose, encryption, application, instance, input, delimiter, separator):

	# Determine what the properties are, from the configuration.
	listen_on = YamlConfig['app_properties']['listen_on']
	if debug or verbose: print("Listen on: " + str(listen_on))

	# Determine what we are to bind to
	if listen_on == "socket":
		socket_addr = YamlConfig['app_properties']['socket_properties']['address']
		socket_port = YamlConfig['app_properties']['socket_properties']['port']
	elif listen_on == "pipe":
		pipe_path = YamlConfig['app_properties']['pipe_path']
	else:
		print("Unknown type to listen on: " + str(listen_on))
		return False

	if listen_on == "socket":
		address = "http://" + socket_addr + ":" + str(socket_port) + "/"

	# Define proxy object
	proxy = xmlrpclib.ServerProxy(address)
	# Call threadedAlert with the following arguments from the defined proxy object.
	result = proxy.threadedAlert(debug, verbose, encryption, application, instance, input, delimiter, separator)

	if verbose:
		print("Result: " + str(result))

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
	instance = False
	input = None
	delimiter = False
	separator = False
	verbose = False
	debug = False
	encryption = False # not implemented(yet?)

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

	# Check if we got the least amount of input
	error = 0
	if not application: print "Missing application name"; error = 1
	if not input: print "Missing input"; error = 1
	if error == 1: sys.exit()

	# Read the config, so it doesnt have to be loaded for every call (downside of reading and parsing for every notifiction)
	if debug or verbose: print("Calling for YamlConfig")
	(temp_result, YamlConfig) = i.load_yaml_config(debug, verbose, None)
	if temp_result:
		if verbose or debug: print(" Configuration data read ")
	else:
		print(" Unable to read the configuration file! ")
		return False

	# Call alert function to pass on the information
	result = doAlert(YamlConfig, debug, verbose, encryption, application, instance, input, delimiter, separator)
	if verbose: 
		if result == 0: 
			print "Result OK: " + str(result)
		else:
			print "Result unknown: " + str(result)

if __name__ == "__main__":
	main()
