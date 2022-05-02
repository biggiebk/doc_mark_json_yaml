#!/usr/bin/python3
"""
	Script used to generate Markdown documenation for JSON files.
"""
import sys
sys.path.append('../doc_mark_json')
import argparse
from doc_mark_json import DocMarkJson

# Lets setup the argument parser
parser = argparse.ArgumentParser(description ='Document generation tool to create '
	+ 'Markdown documents from JSON.')

# Add Arguments
parser.add_argument('input', metavar='Input', help ='File or directory to process')
#parser.add_argument('-out', metavar='OutputDir', action='store', help='Directory for output')

# Parse the arguments
args = parser.parse_args()

# Let's initiate Doctor Mark JSON
doc_mj = DocMarkJson()

# Process
doc_mj.discover(vars(args))

# Lets check for errors
errors = doc_mj.lint()
if errors:
	for error in errors:
		print(error)
	quit()

doc_mj.build()