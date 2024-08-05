# This file is part of Cruscopoetry.
# 
# Cruscopoetry is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Cruscopoetry is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Cruscopoetry. If not, see <http://www.gnu.org/licenses/>.
import tomli
import mum
import os
import pathlib
from .configuration import Configuration
from .elements.daairas import Daaira, DaairaPool
from .elements.feet import Foot, FeetPool
from .elements.metres import Metre, MetrePool
from .elements.metre_forms import MetreForm, MetreFormPool
from .elements.zihaafas import Zihaafa, ZihaafaPool
from .elements.cillas import Cilla, CillaPool
from .foot_namer import FootNamer
from .exceptions import DaairaException


class MetricElements(metaclass=mum.Singleton):
	"""This class reads the configuration file and builds all the instances of all the other classes that represent the various parsing levels of the metre.
	
	Args:
		config_file (str): the path of the configuration file, which must be in TOML language.
	
	Attrs:
		daairas_pool: a DaairaPool containing all the parsed daairas, as instances of the Daaira class
	"""
	
	CONFIG_PATH = "constants.toml"
	
	def __init__(self):
		with open(self.config_file, 'rb') as myfile:
			config_parsing = tomli.load(myfile)

		self.configuration = Configuration(config_parsing)
		del config_parsing["configuration"]
		self.daairas_pool = DaairaPool()
		
		self.foot_namer = FootNamer(self.configuration)

		for daaira in config_parsing["daairas"]:
			self.daairas_pool.add(self._build_daaira(daaira))
		del config_parsing["daairas"]

		self.feet_pool = FeetPool()
		for foot in config_parsing["feet"]:
			self.feet_pool.add(self._build_foot(foot))
		del config_parsing["feet"]
		
		self.metres_pool = MetrePool()
		for metre in config_parsing["metres"]:
			self.metres_pool.add(self._build_metre(metre))
		del config_parsing["metres"]
		
		self.metre_forms_pool = MetreFormPool()
		for metre_form in config_parsing["metre_forms"]:
			self.metre_forms_pool.add(self._build_metre_form(metre_form))
		del config_parsing["metre_forms"]
		
		self.zihaafas_pool = ZihaafaPool()
		for zihaafa in config_parsing["zihaafas"]:
			self.zihaafas_pool.add(self._build_zihaafa(zihaafa))
		del config_parsing["zihaafas"]
		
		self.cillas_pool = CillaPool()
		for cilla in config_parsing["cillas"]:
			self.cillas_pool.add(self._build_cilla(cilla))
		del config_parsing["cillas"]

	@property
	def metre_info_base_16_order(self):
		"""Returns the first power of 16 greater than the maximum int value in self.metre_forms_pool. This value can be used to get the prosodic information from the metadata of an already 
		parsed file, or to write them on it while parsing."""
		maximum_metre_form = max(self.metre_forms_pool.indexes)
		result = 1
		while maximum_metre_form > 0:
			result *= 0x10
			maximum_metre_form //= 0x10
		return result

	@property
	def foot_info_base_16_order(self):
		"""Returns the first power of 16 greater than the maximum int value in self.metre_zihaafas_pool. This value can be used to get the prosodic information from the related field of the section 
		of a JSON file representing a colon, or to store the information on it."""
		maximum_metre_form = max(self.zihaafas_pool.indexes)
		result = 1
		while maximum_metre_form > 0:
			result *= 0x10
			maximum_metre_form //= 0x10
		return result

	@property
	def config_file(self):
		path = pathlib.Path(__file__).parent.resolve()
		path = path.joinpath(self.__class__.CONFIG_PATH)
		return str(path)

	def _build_daaira(self, daaira_dict: dict):
		return Daaira(daaira_dict["index"], daaira_dict["name"], daaira_dict["arabic_name"], daaira_dict["epu_sequence"])
	
	def _build_foot(self, foot_dict: dict):
		return Foot(foot_dict["index"], foot_dict["name"], foot_dict["arabic_name"], foot_dict["epu_sequence"], foot_dict["cillas"])
	
	def _build_metre(self, metre_dict: dict):
		feet_field = metre_dict["feet_sequence"]
		if type(feet_field) == dict:
			daaira = self.daairas_pool[feet_field["from"]]
			try:
				feet_array = daaira.get_feet(feet_field["start_offset"], feet_field["watid_index"])
				feet_array = [self.feet_pool.get_index(foot) for foot in feet_array]
			except DaairaException:
				print("Error while parsing %s"%metre_dict["name"])
				raise
		else:
			feet_array = feet_field
		
		return Metre(metre_dict["index"], metre_dict["name"], metre_dict["arabic_name"], feet_array, metre_dict["forms"])
	
	def _build_metre_form(self, metre_form_dict: dict):
		return MetreForm(metre_form_dict["index"], metre_form_dict["name"], metre_form_dict["arabic_name"], metre_form_dict["aruuds_number"], metre_form_dict["transform"])
	
	def _build_zihaafa(self, zihaafa_dict: dict):
		return Zihaafa(zihaafa_dict["index"], zihaafa_dict["name"], zihaafa_dict["arabic_name"], zihaafa_dict["conditions"], zihaafa_dict["transform"])
	
	def _build_cilla(self, cilla_dict: dict):
		return Cilla(cilla_dict["index"], cilla_dict["name"], cilla_dict["arabic_name"], cilla_dict["in_hashw"], cilla_dict["conditions"], cilla_dict["transform"])
			
	def __str__(self):
		ret_str = ''
		ret_str += str(self.configuration)
		ret_str += os.linesep*2
		ret_str += str(self.daairas_pool)
		ret_str += os.linesep*2
		ret_str += str(self.metres_pool)
		ret_str += os.linesep*2
		ret_str += str(self.metre_forms_pool)
		ret_str += os.linesep*2
		ret_str += str(self.feet_pool)
		ret_str += os.linesep*2
		ret_str += str(self.zihaafas_pool)
		ret_str += os.linesep*2
		ret_str += str(self.cillas_pool)
		ret_str += os.linesep*2
		return ret_str
