# You can run this .tac file directly with:
#    twistd -ny daemon.tac

"""
This is an example .tac file which starts a webserver on port 8080 and
serves files from the current working directory.

The important part of this, the part that makes it a .tac file, is
the final root-level section, which sets up the object called 'application'
which twistd will look for
"""

import os
from twisted.application import service, internet
from twisted.web import static, server
from twisted.protocols import amp
#from interface import NoHaData
#import interface
#reload(interface)

class NoHaAlert(amp.Command):
    arguments = [('debug', amp.Boolean()),
                 ('verbose', amp.Boolean()),
                 ('encryption', amp.Integer()),
                 ('application', amp.String()),
                 ('instance', amp.String()),
                 ('input', amp.String()),
                 ('delimiter', amp.String()),
                 ('separator', amp.String())]
    response = [('result', amp.Boolean())]

class NoHaData(amp.AMP):
    def alert(self, debug, verbose, encryption, application, instance, input, delimiter, separator):
        if encryption:
            print("Not implemented yet")
        else:
            print("No encryption")

        #split to thread and do magic
        if debug or verbose:
            print("Debug:       " + debug)
            print("Verbose:     " + verbose)
            print("Application: " + application)
            print("Instance:    " + instance)
            print("Input:       " + input)
            print("Deliminator: " + delimiter)
            print("Separator    " + separator)

        return {'result': True}
    NoHaAlert.responder(alert)
    def doStart(self):
        return True
    def doStop(self):
        return True

port = 6031
factory = NoHaData()

# this is the important bit
application = service.Application("echo")  # create the Application
echoService = internet.TCPServer(port, factory) # create the service
# add the service to the application
echoService.setServiceParent(application)
