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
import os
from enum import IntEnum


class Configuration:
	"""This class stores the configuration data of the parsers. Moreover, it stores also the enumeration classes of all the elements contained in the configuration file"""

	def __init__(self, dictionary: dict):
		self.json_fields = {key.upper(): value for key, value in dictionary["configuration"].items()}
		
		#now we get the ascii names of the dāʾiras and their integer values:
		self.daairas_enum = self._get_enum_class("DaairasEnum", dictionary["daairas"])
		self.metres_enum  = self._get_enum_class("MetresEnum", dictionary["metres"])
		self.metre_forms_enum  = self._get_enum_class("MetreFormsEnum", dictionary["metre_forms"])
		self.feet_enum  = self._get_enum_class("FeetEnum", dictionary["feet"])
		self.cillas_enum  = self._get_enum_class("CillasEnum", dictionary["cillas"])
		self.zihaafas_enum  = self._get_enum_class("ZihaafasEnum", dictionary["zihaafas"])
	
	def _get_enum_class(self, name: str, dictionary: dict):
		class_dict = {item["ascii_name"].upper(): item["index"] for item in dictionary}
		return IntEnum(name, class_dict)

	
	def __str__(self):
		ret_str = "Configuration:"
		ret_str += os.linesep
		for key, value in self.json_fields.items():
			ret_str += os.linesep + "\t%s = %s"%(key, value)

		ret_str += os.linesep
		ret_str += os.linesep + "\tDaairasEnum:"
		for item in self.daairas_enum:
			ret_str += os.linesep + "\t\t%s = 0x%x"%(item.name, item.value)
		
		ret_str += os.linesep		
		ret_str += os.linesep + "\tMetresEnum:"
		for item in self.metres_enum:
			ret_str += os.linesep + "\t\t%s = 0x%x"%(item.name, item.value)
		
		ret_str += os.linesep
		ret_str += os.linesep + "\tMetreFormsEnum:"
		for item in self.metre_forms_enum:
			ret_str += os.linesep + "\t\t%s = 0x%x"%(item.name, item.value)
		
		ret_str += os.linesep		
		ret_str += os.linesep + "\tFeetEnum:"
		for item in self.feet_enum:
			ret_str += os.linesep + "\t\t%s = 0x%x"%(item.name, item.value)
		
		ret_str += os.linesep		
		ret_str += os.linesep + "\tCillasEnum:"
		for item in self.cillas_enum:
			ret_str += os.linesep + "\t\t%s = 0x%x"%(item.name, item.value)
		
		ret_str += os.linesep		
		ret_str += os.linesep + "\tZihaafasEnum:"
		for item in self.zihaafas_enum:
			ret_str += os.linesep + "\t\t%s = 0x%x"%(item.name, item.value)

		return ret_str
