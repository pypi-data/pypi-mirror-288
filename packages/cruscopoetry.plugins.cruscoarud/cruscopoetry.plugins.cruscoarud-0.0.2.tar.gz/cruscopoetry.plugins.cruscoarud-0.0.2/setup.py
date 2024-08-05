#    This file is part of CruscoArud.
#
#    CruscoArud is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    CruscoArud is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with CruscoArud.  If not, see <http://www.gnu.org/licenses/>.
import os, sys

import setuptools

if __name__ == '__main__':

	with open("README.rst", 'r') as long_file:
		long_descript = long_file.read()

	setuptools.setup(
		name='cruscopoetry.plugins.cruscoarud',
		version='0.0.2',
		package_dir = {"": "src"},
		package_data = {"": ["common/*.toml",]},
		packages=setuptools.find_namespace_packages(where="src", exclude=['tests']),
		entry_points={
			'console_scripts': [
				'cruscoarud = cruscopoetry.plugins.cruscoarud.__main__:CruscoArud.main',
			],
		},
		install_requires=[
			'cruscopoetry.core',
			'cruscopoetry.plugins.abstract',
			"myusefulclasses",
			"myusefulmetaclasses",
			"tomli",
		],
		tests_require=['pytest'],
		author='Emiliano Minerba',
		author_email='emi.nerba@gmail.com',
		description="ʿArūḍ parser for poems in cruscopoetry format",
		long_description=long_descript,
		long_description_content_type='text/x-rst',
		license='GPL',
		url='https://gitlab.com/kikulacho92/cruscopoetry_new',
	)
