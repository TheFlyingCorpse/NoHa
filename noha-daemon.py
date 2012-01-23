#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        noha-daemon.py
# Purpose:     Daemon to handle external calls via pipe and/ socket.
#
# Author:      Rune "TheFlyingCorpse" Darrud
#
# Created:     21.01.2012
# Copyright:   (c) Rune "TheFlyingCorpse" Darrud 2012
# Licence:     GPL 2
#-------------------------------------------------------------------------------

import sys, getopt, xmlrpclib, daemon, time
from SimpleXMLRPCServer import SimpleXMLRPCServer
from logging import Logger
import threading, logging
from threading import Thread
from ruleeval import ruleeval
from interface import interface
import messages

# Make it shorter:
r = ruleeval()
i = interface()

# Puproses which need no explainin
debug = False
verbose = False

# Read the config, so it doesnt have to be loaded for every call (downside to reading and parsing for every notifiction)
(temp_result, YamlConfig) = i.load_yaml_config(debug, verbose, None)
if temp_result:
	# Set up logging before anything else! (Ugly?)
	LoggingEnabled = YamlConfig['app_properties']['logging_properties']['logging_enabled']

	# Use the config (if found) to be the guiding star.
	if LoggingEnabled:
		LogFile = YamlConfig['app_properties']['logging_properties']['logfile']
		LogLevel = YamlConfig['app_properties']['logging_properties']['loglevel']
	else:
		LogFile = '/dev/null'
		LogLevel = 'info'

	LogFormat = YamlConfig['app_properties']['logging_properties']['log_format']
	d={'debug': logging.DEBUG, 'info': logging.INFO, 'warn': logging.WARN, 'error': logging.ERROR, 'critical': logging.CRITICAL}
	logging.basicConfig(filename=LogFile, level=d[LogLevel],format=LogFormat)

	logging.info('Initializing daemon...')
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
    print("  -d, --daemonize       Daemonize")
    print("")
    logging.error(' Usage() called on ' + str(sys.argv[0]))

def doAlert(debug, verbose, encryption, application, instance, input, delimiter, separator):
	logging.warn('Input to doAlert: ')
	logging.warn('  Debug      : ' + str(debug))
	logging.warn('  Verbose    : ' + str(verbose))
	logging.warn('  Application: ' + str(application))
	logging.warn('  Instance   : ' + str(instance))
	logging.warn('  Delimiter  : ' + str(delimiter))
	logging.warn('  Separator  : ' + str(separator))
	logging.warn('  Input: ' + str(input))

	# This is the function we call for now, to be rewritten.
	result = r.eval_input_of_application(debug, verbose, application, instance, input, delimiter, separator)

	# Logging might be handy
	logging.error('Result from server ' + str(result))
	return 0

def main_program(YamlConfig):
    def threadedAlert(debug, verbose, encryption, application, instance, input, delimiter, separator):
        t = Thread(target=doAlert, args=(debug, verbose, encryption, application, instance, input, delimiter, separator))
        t.start()
        return 0

    listen_on = YamlConfig['app_properties']['listen_on']
    if debug or verbose: print("Listen on: " + str(listen_on))
    logging.info('Listen on: ' + str(listen_on))

    # Determine what we are to bind to
    if listen_on == "socket":
        socket_addr = YamlConfig['app_properties']['socket_properties']['address']
        socket_port = YamlConfig['app_properties']['socket_properties']['port']
    elif listen_on == "pipe":
        pipe_path = YamlConfig['app_properties']['pipe_path']
    else:
        logging.info("Unknown type to listen on: " + str(listen_on))
        print("Unknown type to listen on: " + str(listen_on))
        return False

    if listen_on == "socket":
        server = SimpleXMLRPCServer((socket_addr, socket_port))
    else:
        logging.info("Listen on (" + str(listen_on) + ") not implemented yet")
        print("Listen on (" + listen_on + ") not implemented yet")
        return False

    logging.info('Listening on ' + str(socket_addr) + ':' + str(socket_port))
    server.register_function(threadedAlert,"threadedAlert")
    server.serve_forever()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "Dhvd", ["help", "daemonize"])
    except getopt.GetoptError, err:
        #print help information and exit:
        logging.info('Invalid arguments: ' + str(err))
        print(str(err))
        usage()
        sys.exit(2)

    # Set defaults
    verbose = False
    debug = False
    daemonize = False

    # Loop through all arguments
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o == "-D":
            debug = True
        elif o in ("-d", "--daemonize"):
            daemonize = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

    # Call SOME function to pass on the information
    if daemonize:
        logging.info('Daemonizing...')
        with daemon.DaemonContext():
            main_program(YamlConfig)
    else:
        logging.info('Running as a console script...')
        main_program(YamlConfig)

if __name__ == "__main__":
    main()
