#    This file is part of CruscoPoetry.
#
#    CruscoPoetry is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    CruscoPoetry is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with CruscoPoetry.  If not, see <http://www.gnu.org/licenses/>.


#setup file for syllabifiers namespace package
import os

import setuptools

if __name__ == '__main__':

	with open("README.rst", 'r') as long_file:
		long_descript = long_file.read()

	setuptools.setup(
		name='cruscopoetry.syllabifiers.abstract',
		version='0.0.3',
		package_dir = {"": "src"},
		packages=setuptools.find_namespace_packages(where="src"),
		install_requires = [
			"myusefulmetaclasses",
		],
		tests_require = [
			"pytest",
		],
		author='Emiliano Minerba',
		author_email='emi.nerba@gmail.com',
		description="Abstract classes for CruscoPoetry syllabifiers",
		long_description=long_descript,
		long_description_content_type='text/x-rst',
		license='GPL',
		url='https://gitlab.com/kikulacho92/cruscopoetry',
	)
