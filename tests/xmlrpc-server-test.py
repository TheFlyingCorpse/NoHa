#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      TheFlyingCorpse
#
# Created:     22.01.2012
# Copyright:   (c) TheFlyingCorpse 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import time
from threading import Thread


def main():
    import xmlrpclib
    from SimpleXMLRPCServer import SimpleXMLRPCServer

    def is_even(n):
        return n%2 == 0

    def alert(application):
        print("HEI: %s" % application)

    def func(application):
        t = Thread(target=alert, args=(application,))
        t.start()
        return ("application: " + application)

    server = SimpleXMLRPCServer(("localhost", 8000))
    print "Listening on port 8000..."
    server.register_function(is_even, "is_even")
    server.register_function(func,"func")
    server.serve_forever()


if __name__ == '__main__':
    main()

