#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        interface.py
# Purpose:     Contain the rules class and function definitions for the class.
#
# Author:      Rune "TheFlyingCorpse" Darrud
#
# Created:     19.01.2012
# Copyright:   (c) Rune "TheFlyingCorpse" Darrud 2012
# Licence:     GPL 2
#-------------------------------------------------------------------------------

# import OS
import os
# import sys
import sys
# import Regular Expressions
import re
# import pyYAML
import yaml

# import AMP from twisted
from twisted.protocols import amp

class interface:

	def load_app_config(self, debug, verbose, config, application):
		"""
		Return with application specific configuration settings
		"""
		# If config file is unspecified, try to get the default one.
		if not config:
			if debug: print("No config specified, calling for the default one")
			config_result, config = self.load_yaml_config(debug, verbose, None)

		# If application is not set, abort.
		if not application:
			if debug: print("No application specified")
			return False, "No application set, cant return with any properties"

		# Iterate through all known applications
		for item in config['applications']:
			if debug: print("Application read from file: " + str(item))
			# If match
			if item['name'] == application:
				if debug or verbose: print("Got a match for application: " + str(application))
				return True, item
			else:
				if debug or verbose: print("Unknown application specified: " + application)
				return False, "Unknown application specified: " + str(application)

	def load_yaml_config(self, debug, verbose, config_file):
		"""
		Load the application config and return it as (type) dictionary
		"""
		if debug: print("Going to load config data via YaML from: " + str(config_file))
		# Load from default if otherwise specified
		if not config_file:
			if verbose or debug: print("config_file parameter not set, setting it to default path")
			config_file = "etc/noha.yml"

		# Check that it exists before continuing.
		if not self.file_exists(debug, verbose, config_file):
			if verbose or debug: print("Config file could not be located: " + config_file)
			return False, False

		# Open as stream, read-only	
		stream = open(config_file, 'r')

		YamlConfig = yaml.load(stream)
		# Return the data as dictionary type.
		if verbose or debug: print("Config file parsed, returning True, YamlConfig to the calling function with the config structure")
		return True, YamlConfig

	def file_exists(self, debug, verbose, file_path):
		"""
		Check if the file exists.
		"""
		if debug: print("Going to check if file exists: " + file_path)
		if not os.path.isfile(file_path):
			if verbose: print("File not found: " + file_path)
			return False
		
		if verbose: print("File found: " + file_path)
		return True

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

#######################################################################
def main():
    pass

if __name__ == '__main__':
    main()
