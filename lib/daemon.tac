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
#from interface import NoHaData
import interface
reload(interface)

port = 6031
factory = interface.NoHaData()

# this is the important bit
application = service.Application("echo")  # create the Application
echoService = internet.TCPServer(port, factory) # create the service
# add the service to the application
echoService.setServiceParent(application)
