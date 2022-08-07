"""
	Description: Module used integrating with the github wiki
"""
import os
import subprocess
import shutil
from beartype import beartype


class GitWiki():
	"""
		Description: Main class for integration with git wiki
	"""
	@beartype
	def __init__(self, owner: str, repo: str, local_dir: str ) -> None:
		self.owner = owner
		self.repo = repo
		self.local_dir = local_dir
		self.current_dir = ''
	
	@beartype
	def clone(self) -> None:
		"""
			Clones the wiki of the given repo
		"""
		self.__switch_to(self.local_dir)
		print("git", "clone", f"git@github.com:{self.owner}/{self.repo}.wiki.git")
		subprocess.run(["git", "clone", F"git@github.com:{self.owner}/{self.repo}.wiki.git"])
		self.__return_to_current()

	@beartype
	def commit(self, message: str) -> None:
		"""
			Commit the updates
		"""
		self.__switch_to(f"{self.local_dir}/{self.repo}.wiki")
		subprocess.run(["git", "add", "-A"])
		subprocess.run(["git", "commit", "-m", message])
		self.__return_to_current()

	@beartype
	def push(self) -> None:
		"""
			Push to the repo
		"""
		self.__switch_to(f"{self.local_dir}/{self.repo}.wiki")
		subprocess.run(["git", "push"])
		self.__return_to_current()

	@beartype
	def remove(self) -> None:
		"""
			Removes the local wiki directory
		"""
		shutil.rmtree(f"{self.local_dir}/{self.repo}.wiki")

	@beartype
	def __return_to_current(self):
		"""
			Switches to the wiki dir and then returns previous working dir
		"""
		os.chdir(self.current_dir)

	@beartype
	def __switch_to(self, directory):
		"""
			Switches to the wiki dir and then returns previous working dir
		"""
		self.current_dir = os.getcwd()
		os.chdir(directory)
