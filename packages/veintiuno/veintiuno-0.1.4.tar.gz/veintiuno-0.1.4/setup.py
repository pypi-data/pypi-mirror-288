from setuptools import setup, find_packages

with open("./README.md", "r") as rm:
	readme = rm.read()

setup(
	author = "Luis Enrique Quispe Paredes (lequispep@gmail.com)",
	author_email = "lequispep@gmail.com",
	description = "A simple package for create and interact a simple BlackJack environment.",
	long_description = readme,
	long_description_content_type = "text/markdown",
	# url
	# download_url
	# keywords
	# classifiers
	# include_package_data
	license = "MIT",
	name = "veintiuno",
	version = "0.1.4",
	packages = find_packages(include=["veintiuno", "veintiuno.*"]),
	)