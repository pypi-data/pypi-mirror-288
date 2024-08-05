# This file is part of Cruscoarud, a plugin of Cruscopoetry.
# 
# Cruscoarud is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Cruscoarud is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Cruscoarud. If not, see <http://www.gnu.org/licenses/>.


class CruscoArudException(Exception):
	"""Base exception class for all the exceptions and warnings raised by the CruscoArud plugin."""
	
	def __init__(self):
		super().__init__()


class CruscoArudWarning(CruscoArudException):
	"""Base class for all the warnings"""
	
	def __init__(self):
		super().__init__()






































