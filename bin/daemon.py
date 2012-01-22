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

import sys, getopt
sys.path.append('../lib/')
sys.path.append('lib/')
#from ruleeval import ruleeval

# Make it shorter
r = ruleeval()

def usage():
    print(sys.argv[0] + " - Forward notifcations to NoHa")
    print("")
    print("Valid options are:")
    print("  -h, --help            Prints this message")
    print("  -v                    Verbose output")
    print("  -D                    Debug output")
    print("  -d, --daemonize       Daemonize")
    print("")

def daemon():
	print(" NOT IMPLEMENTED  YET")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "Dhv", ["help"])
    except getopt.GetoptError, err:
        #print help information and exit:
        print(str(err))
        usage()
        sys.exit(2)

    # Set defaults
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
        else:
            assert False, "unhandled option"

    # Call SOME function to pass on the information
    daemon()

if __name__ == "__main__":
    main()
