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
import threading
from threading import Thread
from ruleeval import ruleeval
from interface import interface

# Make it shorter:
r = ruleeval()
i = interface()

# Puproses which need no explainin
debug = False
verbose = False

def usage():
    print(sys.argv[0] + " - Forward notifcations to NoHa")
    print("")
    print("Valid options are:")
    print("  -h, --help            Prints this message")
    print("  -v                    Verbose output")
    print("  -D                    Debug output")
    print("  -d, --daemonize       Daemonize")
    print("")

def doAlert(debug, verbose, encryption, application, instance, input, delimiter, separator):
	if verbose and debug:
		print("Thread testing, will print one line every second")
		print("threading info: " + threading.current_thread().name)
		print("DEBUG:       " + str(debug))
		#time.sleep(1)
		print("VERBOSE:     " + str(verbose))
		#time.sleep(1)
		print("INPUT:       " + str(input))
		#time.sleep(1)
		print("APPLICATION: " + str(application))
		#time.sleep(1)
		print("INSTANCE:    " + str(instance))
		#time.sleep(1)
		print("DELIMITER:   " + str(delimiter))
		#time.sleep(1)
		print("SEPARATOR:   " + str(separator))

	# This is the function we call for now, to be rewritten.
	result = r.eval_input_of_application(debug, verbose, application, instance, input, delimiter, separator)

	# Output might be handy
	if verbose or debug: print("Result of eval: " + str(result))
	return 0

def main_program(YamlConfig):
    def threadedAlert(debug, verbose, encryption, application, instance, input, delimiter, separator):
        t = Thread(target=doAlert, args=(debug, verbose, encryption, application, instance, input, delimiter, separator))
        t.start()
        return 0

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
        server = SimpleXMLRPCServer((socket_addr, socket_port))
    else:
        print("Listen on (" + listen_on + ") not implemented yet")
        return False

    print "Listening on port 8000..."
    server.register_function(threadedAlert,"threadedAlert")
    server.serve_forever()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "Dhvd", ["help", "daemonize"])
    except getopt.GetoptError, err:
        #print help information and exit:
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

    # Read the config, so it doesnt have to be loaded for every call (downside of reading and parsing for every notifiction)
    if debug or verbose: print("Calling for YamlConfig")
    (temp_result, YamlConfig) = i.load_yaml_config(debug, verbose, None)
    if temp_result:
        if verbose or debug: print(" Configuration data read ")
    else:
        print(" Unable to read the configuration file! ")
        return False

    # Call SOME function to pass on the information
    if daemonize:
        with daemon.DaemonContext():
            main_program(YamlConfig)
    else:
        main_program(YamlConfig)

if __name__ == "__main__":
    main()
