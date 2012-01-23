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

import logging

interface_logger = logging.getLogger('main_app.interface')

class interface:
	def __init__(self):
		logging.basicConfig(filename='/dev/null', level=logging.INFO, format='%(name)s')
		self.logger = logging.getLogger('main_app')

	def load_app_config(self, debug, verbose, config, application):
		"""
		Return with application specific configuration settings
		"""
		# If config file is unspecified, try to get the default one.
		if not config:
			self.logger.warn(" No config specified, calling for the default one")
			#if debug: print("No config specified, calling for the default one")
			config_result, config = self.load_yaml_config(debug, verbose, None)

		# If application is not set, abort.
		if not application:
			self.logger.warn(" No application specified")
			return False, "No application set, cant return with any properties"

		# Iterate through all known applications
		for item in config['applications']:
			self.logger.error("Application read from file: " + str(item))
			# If match
			if item['name'] == application:
				self.logger.error("Got a match for application: " + str(application))
				return True, item
			else:
				self.logger.info("Unknown application specified: " + str(application))
				return False, "Unknown application specified: " + str(application)

	def load_yaml_config(self, debug, verbose, config_file):
		"""
		Load the application config and return it as (type) dictionary
		"""
		self.logger.warn("Going to load config data via YaML from: " + str(config_file))
		# Load from default if otherwise specified
		if not config_file:
			self.logger.warn("config_file parameter not set, setting it to default path")
			config_file = "etc/noha.yml"

		# Check that it exists before continuing.
		if not self.file_exists(debug, verbose, config_file):
			self.logger.infp("Config file could not be located: " + str(config_file))
			return False, False

		# Open as stream, read-only	
		stream = open(config_file, 'r')

		YamlConfig = yaml.load(stream)
		# Return the data as dictionary type.
		self.logger.warn("Config file parsed, returning True, YamlConfig to the calling function with the config structure")
		return True, YamlConfig

	def file_exists(self, debug, verbose, file_path):
		"""
		Check if the file exists.
		"""
		self.logger.error("Going to check if file exists: " + str(file_path))
		if not os.path.isfile(file_path):
			if verbose: self.logger.warn("File not found: " + str(file_path))
			return False
		
		if verbose: self.logger.error("File found: " + str(file_path))
		return True

#######################################################################
def main():
    pass

if __name__ == '__main__':
    main()
