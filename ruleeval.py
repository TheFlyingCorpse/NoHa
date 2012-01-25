#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        ruleeval.py
# Purpose:     Contain the rules class and function definitions for the class.
#
# Author:      Rune "TheFlyingCorpse" Darrud
#
# Created:     19.01.2012
# Copyright:   (c) Rune "TheFlyingCorpse" Darrud 2012
# Licence:     GPL 2
#-------------------------------------------------------------------------------

# import Regular Expressions
import re
import yaml
import logging

# Import interface
from interface import interface

# make it shorter
i = interface()

ruleeval_logger = logging.getLogger('main_app.ruleeval')

class ruleeval:
    def __init__(self):
		logging.basicConfig(filename='/dev/null', level=logging.INFO, format='%(name)s')
		self.logger = logging.getLogger('main_app')

    def eval_input_of_application(self, config, application, instance, input, input_delimiter, input_separator):
	"""
	UNSAFE!
	Evaluate input of applications
	If no input_delimiter and/ input_separator given, default for application is used.

	Required: application, input
	Optional: instance, input_delimiter, input_separator
	"""

	self.logger.error("Calling for YamlConfig")
	(temp_result, YamlConfig) = i.load_yaml_config(None)

	# Application config (for application in argument)
	if temp_result:
		self.logger.error("Calling for AppConfig")
		(temp_result, AppConfig) = i.load_app_config(YamlConfig, application)

		if (not temp_result) or (repr(AppConfig) is str):
			self.logger.info("Invalid AppConfig data, returning...")
			return False
	else:
		self.logger.info("result of YamlConfig was False(not loaded), not parsing AppConfig, returning early")
		return False

	if not input_delimiter:
		self.logger.error("Setting to default delimiter for application because none are set for input: " + str(AppConfig['delimiter']))
		input_delimiter = AppConfig['delimiter']

	if not input_separator:
		self.logger.error("Setting to default separator for application because none are set for input: " + str(AppConfig['separator']))
		input_separator = AppConfig['separator']

	valid_rules=[]
	# Fetch rules for application + instance and process the conditions to determine valid ones
	for item in i.load_rules_config(YamlConfig):

		self.logger.critical("Rule: " + str(item))

		# Do we have a defined instance(dont skip this rule if not defined)? If instance defined, check if it matches, continue to next rule if no match.
		if item['instance']:
			if item['instance'] != instance:
				continue

		# For easier readability
		rule_conditions=item['conditions']

		for rule_item in rule_conditions:
			filter_match=self.evaluate_input_vs_conditions(input,input_delimiter,input_separator,rule_item)
			print("Filter result: " + str(filter_match))
#		valid_conditions =  self.evaluate_input_vs_conditions(input,input_delimiter,input_separator,condition_list,condition_delimiter,condition_separator)
#		is valid_conditions:
			# Determine if any contacts are set as on-call or shift users.
		
			#contacts_with_methods = self.get_contacts_with_methods_from_rules(valid_condtitions)
			# Determine if contact on holiday
			# Determine if contact on-call
			# More messy code!
	return True

    def evaluate_input_vs_conditions(self, input, input_delimiter, input_separator, rule_conditions_raw):
        """
        Evaluate input vs conditions
        return True if its a valid Rule (what needs to be found is found, and what is not to be found is not found (-: )
        return False if its not a match
        """
        # Convert input string to list
        input_list = self.split_by_separator(input, input_delimiter)

        # Convert rule to sth edible(list)
        rule_conditions = self.split_by_separator(rule_conditions_raw,"\n")

        # Iterate through rules, and try to match against the input
        for item in rule_conditions:
            self.logger.debug("rule_condition_raw: " + str(item))
            if not self.process_lists_to_rule_condition(input_list,input_separator,item):
                self.logger.error("input does not match condition")
                return False
        return True
	
    def process_lists_to_rule_condition(self, input, input_separator, rule_condition_raw):
        """
        Processes a raw rule_condition to a given list and condition
        """
        # Split up the rule into name, operator anv values. (Default values for rule handling for now)
        self.logger.debug("rule_condition_raw: " + str(rule_condition_raw))
        (r_name, r_operator, r_values) = self.split_by_separator_return_first_second_and_third(rule_condition_raw,";",",")

#        input_list = self.split_by_separator_return_first_and_second(input,input_delimiter,input_separator)
        # Treat each entry in the input_list as items.
        for item in input:
            # Name = value from input, per name, eg: HOSTGROUPS=linux-srv,postfix-srv
            self.logger.debug("item: " + str(item))
            (i_name, i_values) = self.split_by_separator_return_first_and_second(item,'=',input_separator)

            # Check if i_name matches r_name, ex: HOSTGROUPS to HOSTGROUPS, then continue
            if i_name == r_name:
                # Return output of condition to valid_condition
                valid_condition = self.compare_list_to_conditions(r_values,i_values,r_operator)

                if valid_condition:
                    continue
                else:
                    # A rule condition failed.
                    self.logger.error("condition failed for rule, '" + str(r_values) + " does not match '" + str(i_values) + "'")
                    return False

        # If everything else goes to plan, return True.
        return True

    def compare_list_to_conditions(self, rule_conditions, input_values, rule_operator):
        """
        Compares a given list with conditions specified.
        """

        # The split up all the conditions to validate.
        condition_result = False

        for condition in rule_conditions:

            # Set the current_sanity to false, because we dont know if its True(rule matches).
            current_condition_result = self.compare_list_with_condition(condition,rule_operator,input_values)

            if current_condition_result:
                condition_result = True

        # Everything matched, then its True
        return condition_result

    def compare_list_with_condition(self, condition, operator, input_list):
        """
        Compare a list with a condition based on regex, exiting based on what the operator is set to.
        """
        # Loop over all input to find matching rules or not.
        for input_item in input_list:
            match_found= self.regex_match_bool(condition, input_item)
            
            if self.result_decider(operator, match_found):
                return True
            else:
                continue

        # Return false, no valid match towards operator.
        return False

    def regex_match_bool(self, string1, string2):
        """
        Do regex matching of strings, return a Bool type as result.
        """
        self.logger.error("string1: " + str(string1))
        self.logger.error("string2: " + str(string2))
        match = re.match(string1, string2)
        if match:
            self.logger.error("match from regex is True")
            return True
        else:
            self.logger.error("match from regex is False")
            return False

    def result_decider(self, operator, match_found):
        """
        Decide what result to return with, based on operator given.
        Ex1: if Operator & and it its found, return True, True
        Ex2: if Operator ! and its not found, return True, False
        Ex3: if Operator | and its not found, return True, False
        Ex4: if Operator ! and its found, return False, True
        """
        # If Match Required, Match Found and Operator
        if ((operator == "&" or operator == "|") and match_found):
            return True
        elif ((operator == "&" or operator == "|") and not match_found):
            return False
        elif (operator == "!" and match_found):
            return False
        elif (operator == "!" and not match_found):
            return True
        else:
            self.logger.info("Unknown combination, operator: " + str(operator) + " match_found: " + str(match_found))
            return False

    def split_by_separator(self, string, separator):
        """
        Splits by given separator
        """
        return string.split(separator)

    def split_by_separator_return_first(self, string, separator):
        """
        Returns the first entry in list
        """
        self.logger.debug("string: " + str(string))
        self.logger.debug("separator: " + str(separator))
        list = string.split(separator)
        self.logger.debug("list[0]: " + str(list[0]))
        return list[0]

    def split_by_separator_return_second(self, string, separator):
        """
        Returns the second entry in list
        """
        self.logger.debug("string: " + str(string))
        self.logger.debug("separator: " + str(separator))
        list = string.split(separator)
        self.logger.debug("list[1]: " + str(list[1]))
        return list[1]

    def split_by_separator_return_first_and_second(self, string, first_separator, second_separator):
        """
        Returns the first and second entry in list
        """
        self.logger.debug("string: " + str(string))
        self.logger.debug("first_separator: " + str(first_separator))
        self.logger.debug("second_separator: " + str(second_separator))
        list1 = string.split(first_separator)
        self.logger.debug("list1[0]: " + str(list1[0]))
        list2 = list1[1].split(second_separator)
        self.logger.debug("list2: " + str(list2))

        return (list1[0], list2)

    def split_by_separator_return_first_second_and_third(self, string, first_separator, second_separator):
        """
        Returns the first, second and third(rest) entry in list
        """
        list1 = string.split(first_separator)
        self.logger.debug("string: " + str(string))
        self.logger.debug("first_separator: " + str(first_separator))
        self.logger.debug("second_separator: " + str(second_separator))
        self.logger.debug("list1[0]: " + str(list1[0]))
        self.logger.debug("list1[1]: " + str(list1[1]))
        list2 = list1[2].split(second_separator)
        self.logger.debug("list2: " + str(list2))

        return (list1[0], list1[1], list2)

#######################################################################
def main():
    pass

if __name__ == '__main__':
    main()
