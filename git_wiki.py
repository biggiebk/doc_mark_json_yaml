"""
	Description: Module used integrating with the github wiki
"""
import os
import subprocess
from beartype import beartype


class GitWiki():
	"""
		Description: Main class for integration with git wiki
	"""
	@beartype
	def __init__(self, user: str, repo: str, local_dir: str ) -> None:
		self.user = user
		self.repo = repo
		self.local_dir = local_dir
		self.current_dir = ''
	
	@beartype
	def clone(self) -> None:
		"""
			Clones the wiki of the given repo
		"""
		subprocess.run(["git", "clone", f"git@github.com:{self.user}/{self.repo}.wiki"])

	@beartype
	def commit(self, message: str) -> None:
		"""
			Commit the updates
		"""
		self.__switch_to_wiki()
		subprocess.run(["git", "add", "-A"])
		subprocess.run(["git", "commit", "-m", message])
		self.__return_to_current()

	@beartype
	def push(self) -> None:
		"""
			Push to the repo
		"""
		self.__switch_to_wiki()
		subprocess.run(["git", "push"])
		self.__return_to_current()

	@beartype
	def __return_to_current(self):
		"""
			Switches to the wiki dir and then returns previous working dir
		"""
		os.chdir(self.current_dir)

	@beartype
	def __switch_to_wiki(self):
		"""
			Switches to the wiki dir and then returns previous working dir
		"""
		self.current_dir = os.getcwd()
		os.chdir(self.local_dir)
