"""
	Description: Module used for parsing JSON files and converting to markdown
"""

import os
import glob
import json
import yaml
from typing import Union
from beartype import beartype
from jinja2 import Environment, PackageLoader, select_autoescape

class DocMarkJson():
	"""
		Description: Main class for reading in and parsing JSON files
	"""
	@beartype
	def __init__(self, defaults: dict[str, Union[str, int, bool]] = None ) -> None:
		""" Construct for DocMarkJson """
		if defaults is None:
			defaults = { 'html': False, 'out': None }
		self.parameters = defaults
		self.directories = {}

	@beartype
	def build(self) -> None:
		"""
			Builds the mark down files
		"""
		for directory, files in self.directories.items(): # For each directory
			for filename in files: ## For each file in the directory
				with open(F"{directory}/{filename}", 'r', encoding='utf-8') as file:
					file_data = file.read()
				file_dict = {}
				if F"{directory}/{filename}".endswith('json'):
					file_dict = self.__load_json(file_data)
				if F"{directory}/{filename}".endswith('yaml') or F"{directory}/{filename}".endswith('yml'):
					file_dict = self.__load_yaml(file_data)
				if not 'template' in file_dict['document']:
					file_dict['document']['template'] = 'default.md.j2'
				env = Environment( loader=PackageLoader("doc_mark_json"), autoescape=select_autoescape())
				template = env.get_template(file_dict['document']['template'])
				with open(F"{self.parameters['out']}/{os.path.splitext(filename)[0]}.md", "w",
				encoding='utf-8')as markdown_file:
					markdown_file.write(template.render(document=file_dict['document']))
				markdown_file.close()

	@beartype
	def discover(self, parameters: dict[str, Union[str, int, bool]]) -> None:
		"""
			Discover files based on parameters provided
			Requires:
				Parameters - Dictionary containing required various parameters.
				The following is required:
					* input - Path to a JSON file or a directory to process
				Optional:
					* out - Path to the output directory.  Default is to create a md directory in the same
					        directory as the specfied file or the directory specified.
		"""
		# Reset directories
		self.directories = {}
		# Does input exist
		if os.path.exists(parameters['input']):
			# Let's set the input to abosulte path before we continue
			parameters['input'] = os.path.abspath(parameters['input'])
			# Is it a file
			if os.path.isfile(parameters['input']):
				# Add directory and file name to parameters
				(directory, filename) = os.path.split(parameters['input'])
				self.directories[directory] = [filename]
			# Is it a directory
			if os.path.isdir(parameters['input']):
				self.directories = { parameters['input']: [] }
				# Look for JSON
				self.__find_files(parameters, 'json')
				# Look for YAML
				self.__find_files(parameters, 'yaml')
				self.__find_files(parameters, 'yml')
		else: # File does not exist throw error
			raise OSError(f"{parameters['input']} does not exist!")

		self.parameters.update(parameters)
		# Set the out directory to input if not specified
		if self.parameters['out'] is None:
			self.parameters['out'] = self.parameters['input']
		else:
			self.parameters['out'] = os.path.abspath(parameters['out'])

	@beartype
	def lint(self) -> list:
		"""
			Looks for errors in the files
		"""
		errors = []
		for directory, files in self.directories.items(): # For each directory
			for filename in files: ## For each file in the directory
				with open(F"{directory}/{filename}", 'r', encoding='utf-8') as file:
					file_data = file.read()
				try:
					if F"{directory}/{filename}".endswith('json'):
						self.__load_json(file_data)
				except json.JSONDecodeError as xcpt:
					errors.append(f"Failed to decode: {directory}/{filename}\n" +
						f"\t{xcpt.msg} Line: {xcpt.lineno} Col: {xcpt.colno}")
		return errors

	@beartype
	def __find_files(self, parameters: dict[str, Union[str, int, bool]], extension: str):
		""" Search for files given specific extension """
		# Lets build the filenames array
		for path_to_file in glob.glob(f"{parameters['input']}/*.{extension}"):
			if os.path.isfile(path_to_file):
				(directory, filename) = os.path.split(path_to_file)
				self.directories[parameters['input']].append(filename)

	def __load_json(self, data: str) -> dict:
		""" Loads JSON and returns dict """
		return json.loads(data) # Can we read the file

	def __load_yaml(self, data: str) -> dict:
		""" Loads YAML and returns dict """
		return yaml.loads(data) # Can we read the file
