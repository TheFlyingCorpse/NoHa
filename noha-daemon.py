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
import threading, logging
from threading import Thread
from ruleeval import ruleeval
from interface import interface

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
	LoggingEnabled = YamlConfig['app_properties']['daemon_logging_properties']['logging_enabled']

	# Use the config (if found) to be the guiding star.
	if LoggingEnabled:
		LogFile = YamlConfig['app_properties']['daemon_logging_properties']['logfile']
		LogLevel = YamlConfig['app_properties']['daemon_logging_properties']['loglevel']
	else:
		LogFile = '/dev/null'
		LogLevel = 'info'

	LogFormat = YamlConfig['app_properties']['daemon_logging_properties']['log_format']
	d={'debug': logging.DEBUG, 'info': logging.INFO, 'warn': logging.WARN, 'error': logging.ERROR, 'critical': logging.CRITICAL}

    # Load the basic config for the logging module.
	logging.basicConfig(filename='/dev/null', level=d[LogLevel], format=LogFormat)
	daemon_logger = logging.getLogger('main_app')
	daemon_logger.setLevel(d[LogLevel])
	fh = logging.FileHandler(LogFile)
	fh.setLevel(d[LogLevel])
	formatter = logging.Formatter(LogFormat)
	fh.setFormatter(formatter)
	daemon_logger.addHandler(fh)

	daemon_logger.info('Initializing daemon...')
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
    daemon_logger.error(' Usage() called on ' + str(sys.argv[0]))

def doAlert(debug, verbose, application, instance, input, delimiter, separator):
	daemon_logger.warn('Input to doAlert: ')
	daemon_logger.warn('  Debug      : ' + str(debug))
	daemon_logger.warn('  Verbose    : ' + str(verbose))
	daemon_logger.warn('  Application: ' + str(application))
	daemon_logger.warn('  Instance   : ' + str(instance))
	daemon_logger.warn('  Delimiter  : ' + str(delimiter))
	daemon_logger.warn('  Separator  : ' + str(separator))
	daemon_logger.warn('  Input: ' + str(input))

	# This is the function we call for now, to be rewritten.
	result = r.eval_input_of_application(debug, verbose, application, instance, input, delimiter, separator)

	# Logging might be handy
	daemon_logger.error('Result from server ' + str(result))
	return 0

def main_program(YamlConfig):
    def threadedAlert(debug, verbose, application, instance, input, delimiter, separator):
        t = Thread(target=doAlert, args=(debug, verbose, application, instance, input, delimiter, separator))
        t.start()
        return 0

    connection_type = YamlConfig['app_properties']['connection_type']
    if debug or verbose: print("Listen on: " + str(connection_type))
    daemon_logger.info('Listen on: ' + str(connection_type))

    # Determine what we are to bind to
    if connection_type == "socket":
        socket_addr = YamlConfig['app_properties']['socket_properties']['address']
        socket_port = YamlConfig['app_properties']['socket_properties']['port']
    elif connection_type == "pipe":
        pipe_path = YamlConfig['app_properties']['pipe_path']
    else:
        daemon_logger.info("Unknown connection type to listen on: " + str(connection_type))
        print("Unknown connection type to listen on: " + str(connection_type))
        return False

    if connection_type == "socket":
        server = SimpleXMLRPCServer((socket_addr, socket_port))
    else:
        daemon_logger.info("Connection type " + str(connection_type) + " not implemented yet")
        print("Connection type " + connection_type + " not implemented yet")
        return False

    daemon_logger.info('Listening on ' + str(socket_addr) + ':' + str(socket_port))
    server.register_function(threadedAlert,"threadedAlert")
    server.serve_forever()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "Dhvd", ["help", "daemonize"])
    except getopt.GetoptError, err:
        #print help information and exit:
        daemon_logger.info('Invalid arguments: ' + str(err))
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
        daemon_logger.info('Daemonizing...')
        with daemon.DaemonContext():
            main_program(YamlConfig)
    else:
        daemon_logger.info('Running as a console script...')
        main_program(YamlConfig)

if __name__ == "__main__":
    main()
