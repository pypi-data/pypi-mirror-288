# This file is part of CruscoPoetry.
# 
# CruscoPoetry is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# CruscoPoetry is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with CruscoPoetry. If not, see <http://www.gnu.org/licenses/>.

from ..exceptions import CruscoArudException


class CruscoArudRenderingException(CruscoArudException):

	def __init__(self):
		super().__init__()


class TextNotParsedException(CruscoArudRenderingException):

	def __init__(self, poem_title: str):
		super().__init__()
		self.poem_title = poem_title
	
	def __str__(self):
		return "The poem '"+ self.poem_title +"' must be parsed before being rendered. Please use the parse function of this plugin"
