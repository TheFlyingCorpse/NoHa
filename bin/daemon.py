#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        daemon.py
# Purpose:     Daemon to handle external calls via pipe and/ socket.
#
# Author:      Rune "TheFlyingCorpse" Darrud
#
# Created:     21.01.2012
# Copyright:   (c) Rune "TheFlyingCorpse" Darrud 2012
# Licence:     GPL 2
#-------------------------------------------------------------------------------

import sys, getopt, xmlrpclib, daemon
from SimpleXMLRPCServer import SimpleXMLRPCServer
from threading import Thread

sys.path.append('../lib/')
sys.path.append('lib/')
#from ruleeval import ruleeval

# Make it shorter
#r = ruleeval()

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
	if verbose or debug:
		print "DEBUG:       " + str(debug)
		print "VERBOSE:     " + str(verbose)
		print "INPUT:       " + str(input)
		print "APPLICATION: " + str(application)
		print "INSTANCE:    " + str(instance)
		print "DELIMITER:   " + str(delimiter)
		print "SEPARATOR:   " + str(separator)
	return 0

def main_program():
    def threadedAlert(debug, verbose, encryption, application, instance, input, delimiter, separator):
        t = Thread(target=doAlert, args=(debug, verbose, encryption, application, instance, input, delimiter, separator))
        t.start()
        return 0

    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
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

    # Call SOME function to pass on the information
    if daemonize:
        with daemon.DaemonContext():
            main_program()
    else:
        main_program()

if __name__ == "__main__":
    main()
