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
import interface
import logging

# Make it shorter
i = interface.interface()

debug = False
verbose = False

# Read the config, so it doesnt have to be loaded for every call (downside to reading and parsing for every notifiction)
(temp_result, YamlConfig) = i.load_yaml_config(debug, verbose, None)
if temp_result:
    # Set up alert_logger.before anything else! (Ugly?)
    LoggingEnabled = YamlConfig['app_properties']['alert_logging_properties']['logging_enabled']

    # Use the config (if found) to be the guiding star.
    if LoggingEnabled:
        LogFile = YamlConfig['app_properties']['alert_logging_properties']['logfile']
        LogLevel = YamlConfig['app_properties']['alert_logging_properties']['loglevel']
    else:
        LogFile = '/dev/null'
        LogLevel = 'info'

    # Logformat
    LogFormat = YamlConfig['app_properties']['alert_logging_properties']['log_format']

    # key to object for alert_logger.options.
    d={'debug': logging.DEBUG, 'info': logging.INFO, 'warn': logging.WARN, 'error': logging.ERROR, 'critical': logging.CRITICAL}

    # Load the basic config for the logging function.
    logging.basicConfig(filename='/dev/null', level=d[LogLevel], format=LogFormat)
    alert_logger = logging.getLogger('main_app')
    alert_logger.setLevel(d[LogLevel])
    fh = logging.FileHandler(LogFile)
    fh.setLevel(d[LogLevel])
    formatter = logging.Formatter(LogFormat)
    fh.setFormatter(formatter)
    alert_logger.addHandler(fh)

    alert_logger.warn('Sending alert...')
    # Logging done, lets get on to business...
else:
    print("Could not read the configuration, unable to proceed")
    sys.exit(2)

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

def doAlert(debug, verbose, application, instance, input, delimiter, separator):

	# Determine what the properties are, from the configuration.
	connection_type = YamlConfig['app_properties']['connection_type']
	if debug or verbose: print("Connect via: " + str(connection_type))
	alert_logger.error('Method to use: ' + str(connection_type))

	# Determine what we are to bind to
	if connection_type == "socket":
		socket_addr = YamlConfig['app_properties']['socket_properties']['address']
		socket_port = YamlConfig['app_properties']['socket_properties']['port']
	elif connection_type == "pipe":
		pipe_path = YamlConfig['app_properties']['pipe_path']
	else:
		print("Unknown connection type to connect with: " + str(connection_type))
		alert_logger.info('Unknown connection type to connect with: ' + str(connection_type))
		return False

	if connection_type == "socket":
		address = "http://" + socket_addr + ":" + str(socket_port) + "/"
		alert_logger.warn('Address to connect to: ' + str(address))

	# Define proxy object
	proxy = xmlrpclib.ServerProxy(address)
	# Call threadedAlert with the following arguments from the defined proxy object.
	result = proxy.threadedAlert(application, instance, input, delimiter, separator)

	if verbose:
		print("Result: " + str(result))
	alert_logger.error('Result from server: ' + str(result))

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "Dvha:Ii:d:s:", ["help", "application=", "instance=", "input=", "delimiter=", "separator="])
	except getopt.GetoptError, err:
		#print help information and exit:
		print(str(err))
		alert_logger.exception(err)
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
	if not application: print "Missing application name"; error = 1; alert_logger.info('Missing application name as an argument!')
	if not input: print "Missing input"; error = 1; alert_logger.info('Missing input as argument!')
	if error == 1: alert_logger.info('Exiting prematurely because of missing arguments');sys.exit()

	# Read the config, so it doesnt have to be loaded for every call (downside of reading and parsing for every notifiction)
	if debug or verbose: print("Calling for YamlConfig")
	(temp_result, YamlConfig) = i.load_yaml_config(debug, verbose, None)
	if temp_result:
		if verbose or debug: print(" Configuration data read ")
	else:
		print(" Unable to read the configuration file! ")
		return False

	# Call alert function to pass on the information, incase of error level debug, log the data.
	alert_logger.error('Calling doAlert with the following arguments: ')
	alert_logger.error('  Debug       : ' + str(debug))
	alert_logger.error('  Verbose     : ' + str(verbose))
	alert_logger.error('  Application : ' + str(application))
	alert_logger.error('  Instance    : ' + str(instance))
	alert_logger.error('  Delimiter   : ' + str(delimiter))
	alert_logger.error('  Separator   : ' + str(separator))
	alert_logger.error('  Input: ' + str(input))

	result = doAlert(debug, verbose, application, instance, input, delimiter, separator)
	if verbose: 
		if result == 0: 
			print "Result OK: " + str(result)
		else:
			print "Result unknown: " + str(result)

	# Log result if its critical or more.
	alert_logger.error('Result from doAlert: ' + str(result))

if __name__ == "__main__":
	main()
