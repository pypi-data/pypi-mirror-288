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
from ..exceptions import CruscoArudException, CruscoArudWarning


class MorePossibleParsingsWarning(CruscoArudWarning):
	"""Raised when a HemistichParser object returns more than a possible parsing."""
	
	def __init__(self, parsings: list):
		super().__init__()
		self._parsings = parsings
	
	@property
	def parsings(self):
		return self._parsings
	
	def __str__(self):
		return "\u001b[1;33mWarning: more than a possible parsing found: %r\u001b[0m"%([parsing.as_tuple for parsing in self.parsings],)


class ParsingException(CruscoArudException):
	"""Base class for the exceptions related to parsing"""
	
	def __init__(self):
		super().__init__()
		

class MetreFormError(ParsingException):

	def __init__(self, metre, form):
		super().__init__()
		self.metre = metre
		self.form = form
	
	def __str__(self):
		return "The %s metre does not accept the %s form."%(self.metre.name, self.form.name)


class StorageError(ParsingException):
	"""Raised when one tries to store a line_parsing on a JsonLine instance containing a different number of cola."""
	
	def __init__(self, line_parsing, json_line):
		super().__init__()
		self._line_parsing = line_parsing
		self._json_line = json_line
	
	def __str__(self):
		return "Impossible to store parsing of %d cola in line of %d"%(len(self._line_parsing.cola_parsings), json_line.count_cola())


class NotMatchingColaNumberError(ParsingException):
	"""Raised when the parse method of a LineParser instance is called on a JsonLine object whose number of cola does not correspond to that of the line parser"""
	
	def __init__(self, form, line):
		super().__init__()
		self._form = form
		self._line = line
	
	def __str__(self):
		"""Line of %d cola can not be parsed by a %s metre form"""%(line.count_cola(), self.form.name)


class FailedParsingException(ParsingException):
	"""Raised when a hemistich parsing returns no acceptable parsing."""
	
	WARNING = 33
	ERROR = 31
	
	def __init__(self):
		super().__init__()
		self.colon_number: int = 0
		self.line_number: int = 0
		self.metre: str = ""
		self.form: str = ""
		self.color: int = self.__class__.ERROR
		self.harfs: str = ""
		
	def __str__(self):
		return "\u001b[1;%dmFailed parsing colon %d of line %d with metre '%s %s'\u001b[0m"%(self.color, self.colon_number, self.line_number, self.metre, self.form)

