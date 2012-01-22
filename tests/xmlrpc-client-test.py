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

def main():
    import xmlrpclib

    proxy = xmlrpclib.ServerProxy("http://localhost:8000/", allow_none=True)
    #print "3 is even: %s" % str(proxy.is_even(3))
    application='icinga'
    instance='fak'
    debug=False
    verbose=False
    encryption=None
    input="FEU FEI"
    delimiter=";"
    separator=","

    print "Call wierd function: %s" % str(proxy.threadedAlert(debug, verbose, encryption, application, instance, input, delimiter, separator))

if __name__ == '__main__':
    main()

