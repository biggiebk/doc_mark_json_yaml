#!/usr/local/bin/python3.10
"""
	Script to convert files between yaml and json formats
"""
import json
import yaml
import argparse


# Lets setup the argument parser
parser = argparse.ArgumentParser(description ='Convert files between JSON and YAML Formats')


# Add Arguments
parser.add_argument('to', metavar='To', choices=['json', 'yaml', 'yml'], help ='Format to convert to')
parser.add_argument('file', metavar='File', help='Oringal file to convert from')

# Parse the arguments
args = parser.parse_args()

# Load the file data
with open(args.file, 'r', encoding='utf-8') as file:
	file_data = file.read()

# If JSON convert to YAML
if args.to == 'json':
	save_file = args.file.rstrip('yaml')
	file_dict = yaml.safe_load(file_data)
	with open(f"{save_file}json", 'w', encoding ='utf8') as file_out:
		json.dump(file_dict, file_out)
else:
	save_file = args.file.rstrip('json')
	file_dict = json.loads(file_data)
	with open(f"{save_file}yaml", 'w', encoding ='utf8') as file_out:
		yaml.dump(file_dict, file_out)
