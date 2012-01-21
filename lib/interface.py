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

class interface:

	def load_app_config(self, config_file):
		"""
		Load the application config and return it as (type) dictionary
		"""
		# Load from default if otherwise specified
		if not config_file:
			config_file = "../etc/noha.yml"

		# Check that it exists before continuing.
		if not self.file_exists(config_file):
			return False, "Config file could not be located: " + config_file

		# Open as stream, read-only	
		stream = open(config_file, 'r')

		appConfig = yaml.load(stream)
		# Return the data as dictionary type.
		return True, appConfig

	def file_exists(self, file_path):
		"""
		Check if the file exists.
		"""
		if not os.path.isfile(file_path):
			return False
		
		return True

#######################################################################
def main():
    pass

if __name__ == '__main__':
    main()
