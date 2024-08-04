import typing

import setuptools


def load_req() -> typing.List[str]:
	with open('requirements.txt') as f:
		return f.readlines()


VERSION = ""
with open("multi_notifier/__version__.py") as f:
	for line in f:
		if line.startswith("__version__"):
			VERSION = line.split('"')[1]

setuptools.setup(
	name="multi_notifier",
	version=VERSION,
	author="Seuling N.",
	description="notify multiple recipients on multiple protocols",
	long_description="notify multiple recipients on multiple protocols",
	packages=setuptools.find_packages(exclude=["tests*"]),
	install_requires=load_req(),
	python_requires=">=3.10",
	license="Apache License 2.0"
)
