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
from ..common.metric_elements import MetricElements
from ..common.elements.cillas import Cilla
from ..common.elements.feet import Foot
from typing import Tuple
from .zihaafa_parser import ZihaafaParser, ZihaafaParsing
from muc import SubscriptableSet


class CillaParsing:
	"""Represents the result of a successful parsing operated by a CillaParser instance"""

	def __init__(self, foot: Foot, cilla: Cilla, zihaafa_parsing: ZihaafaParsing):
		self._foot = foot
		self._cilla = cilla
		self._zihaafa_parsing = zihaafa_parsing
	
	@property
	def foot(self):
		return self._foot
	
	@property
	def cilla(self):
		return self._cilla
	
	@property
	def zihaafa(self):
		return self._zihaafa_parsing.zihaafa
	
	@property
	def length(self):
		return self._zihaafa_parsing.length
		
	def __len__(self):
		return self.length
	
	@property
	def variation_level(self) -> int:
		"""Returns an integer which gives an approximate idea of how the parsed foot is far from the base form (the higher the integer is, the further is the form)"""
		ret_int = self.cilla.variation_level
		ret_int += self.zihaafa.variation_level
		return ret_int
		
	@property
	def json_number(self):
		"""The number that will represent this result in the JSON file"""
		return int(self.cilla) * 0x10 + int(self.zihaafa)
		
	@property
	def as_tuple(self):
		"""Returns the integer of the foot, the ʿilla and the ziḥāfa in a tuple"""
		return (int(self.foot), int(self.cilla), int(self.zihaafa))
	
	def __repr__(self):
		return "%s(%s, %s, %s)"%(self.__class__.__name__, self.foot.name, self.cilla.name, self.zihaafa.name)


class CillaParser:
	"""Parses a sequence of ḥarf values, confronting it with all the possible *ziḥāfa* variations that the represented ʿilla can have. Objects of this class are indexable, and can therefore be 
	collected in a SubscriptableSet.
	
	Args:
		cilla (Cilla): the ʿilla from which this CillaParser instance is created
		sequence (Tuple[str]): a sequence of ḥarf values, representing the foot affected by the ʿilla
		watid_index: the index at which one finds in sequence the EPU corresponding to the *watid*.
	"""

	def __init__(self, cilla: Cilla, foot: Foot, from_hashw: bool = True, elements: MetricElements = None):
		self._elements = elements if elements != None else MetricElements()
		self._cilla = cilla
		self._foot = foot
		self._sequence = cilla.transform(foot)
		self._base_sequence = foot.epu_sequence
		self._from_hashw = from_hashw
		self._is_kharm = int(cilla) == self._elements.configuration.cillas_enum.KHARM
		
		#in order to get the ziḥāfāt, first we need to know which are possible for the base sequence (as from_kharm parametre, we obviously set False):
		zihaafas = SubscriptableSet(zihaafa for zihaafa in self._elements.zihaafas_pool if zihaafa.is_possible(self._foot.epu_sequence, self._foot.watid_index, False))
		
		#then we filter them, removing those which are not applicable in the changed sequence:
		if int(self._cilla) != self._elements.configuration.cillas_enum.NOTHING:
			zihaafas = SubscriptableSet(zihaafa for zihaafa in zihaafas if zihaafa.is_possible(self._sequence, self._foot.watid_index, self._is_kharm))
		
		
		#before we go on, we have to handle some particular cases which require the elimination of some of the possible ziḥāfāt:
		
		#if ʿilla is tasbīġ:
		#	if foot._base_sequence is of 3 epus, we need to remove kaff and šakl from the ziḥāfas; 
		#	if foot._base_sequence is of 2 epus, we need to remove qabḍ from the ziḥāfas
		 
		if int(self._cilla) == self._elements.configuration.cillas_enum.TASBIIGH:
			if len(self._base_sequence) == 2:
				zihaafas.pop(self._elements.configuration.zihaafas_enum.QABD)
			elif len(self._base_sequence) == 3:
				zihaafas.pop(self._elements.configuration.zihaafas_enum.KAFF)
				zihaafas.pop(self._elements.configuration.zihaafas_enum.SHAKL)

		#if ʿilla is qaṣr or ḥaḏf:
		#	if foot._base_sequence is of 3 epus, we need to remove qaṣr from the ziḥāfas;
		if int(self._cilla) in (self._elements.configuration.cillas_enum.QASR, self._elements.configuration.cillas_enum.HADHF):
			if len(self._base_sequence) == 3:
				zihaafas.pop(self._elements.configuration.zihaafas_enum.QABD)
				
		#if the foot is fāʿi_lātun (which has no ʿilla variations), we need to remove qabḍ:
		if int(self._foot) == self._elements.configuration.feet_enum.FAACI_LAATUN:
			zihaafas.pop(self._elements.configuration.zihaafas_enum.QABD)



		#now we can form the ZihaafaParser instances.
		self.zihaafa_parsers = SubscriptableSet(ZihaafaParser(zihaafa, self._sequence, from_hashw, self._is_kharm) for zihaafa in zihaafas)
		

	@property
	def sequence(self):
		return self._sequence

	def __str__(self):
		return self._cilla.name + ": " + str(self._sequence)

	def __index__(self):
		return int(self._cilla)		

	def parse(self, harfs: str, full_match: bool = False) -> Tuple[CillaParsing]:
		"""Takes a string of ḥarf values. If self._from_hashw == True, returns all the zihaafas that match its beginning in a CillaParsing instance; if self._from_haswh == False, it checks the 
		matching at the string's end.
		
		Args:
			harfs (str): the string of ḥarf values
			full_match (bool): default False. If True, the parser checks that the entire string `harfs` matchs the parsing.
		
		Returns:
			parsing (CillaParsing): the results of the parsing, or None if the parsing was not successful.
		"""
		results = [zihaafa_parser.parse(harfs, full_match) for zihaafa_parser in self.zihaafa_parsers]
		
		results = [result for result in results if result != None]
		
		#now we remove from result those ḥašw-parsings which would leave a silent ḥarf as first letter of the following foot:
		if self._from_hashw:
			for i in range(len(results)-1, -1, -1):
###				print("\u001b[1;33m%s\u001b[0m"%results[i].zihaafa.name)
###				print("\u001b[1;33m%s %s\u001b[0m"%(harfs[:results[i].length], harfs[results[i].length:]))
###				print("\u001b[1;33m" + "-"*(results[i].length) + "!" + "\u001b[0m")
				if len(harfs) > results[i].length:
					if harfs[results[i].length] == "1":
###						print("\u001b[1;31m%s leaves a 1 after\u001b[0m"%results[i].zihaafa.name)
						results.pop(i)
		
		results = tuple(results)
		
		if len(results) == 0:
			return None
			
###		if len(results) > 1:
###			print("\u001b[1;33mWarning. More than a ZihaafaParsing with Cilla Parser '%s' found:\u001b[0m"%str(self))
###			print(tuple(str(result) for result in results))
		
		return tuple(CillaParsing(self._foot, self._cilla, result) for result in results)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
