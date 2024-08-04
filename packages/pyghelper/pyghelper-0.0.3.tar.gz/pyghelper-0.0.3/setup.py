import setuptools

with open("README.md", "r", encoding="utf-8") as fi:
    long_description = fi.read()

setuptools.setup(
	name="pyghelper",
	version="0.0.3",
	author="Paul 'charon25' Kern",
	description="Functions and classes to help use PyGame (WIP)",
	long_description=long_description,
    long_description_content_type='text/markdown',
	python_requires=">=3.11",
	url="https://www.github.com/charon25/PythonGameHelper",
	license="MIT",
	packages=['pyghelper'],
	install_requires=[
		'pygame>=2.0.1'
	]
)