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
from mum import Singleton
from .configuration import Configuration


class FootNamer(metaclass=Singleton):

	def __init__(self, configuration: Configuration):
		self._ARABIC = False
		self._configuration = configuration

	@property
	def ARABIC(self):
		return self._ARABIC
	
	@ARABIC.setter
	def ARABIC(self, value: bool):
		self._ARABIC = value
	
	@property
	def feet_enum(self):
		return self._configuration.feet_enum
	
	@property
	def cillas_enum(self):
		return self._configuration.cillas_enum
	
	@property
	def zihaafas_enum(self):
		return self._configuration.zihaafas_enum
			
	@property
	def SAALIM(self):
		if not self.ARABIC:
			return "sālim"
		else:
			return "سالم"
			
	@property
	def CADB(self):
		if not self.ARABIC:
			return "ʿaḍb"
		else:
			return "عضب"
			
	@property
	def MACDUUB(self):
		if not self.ARABIC:
			return "maʿḍūb"
		else:
			return "معضوب"
			
	@property
	def ATHLAM(self):
		if not self.ARABIC:
			return "aṯlam"
		else:
			return "أثلم"
			
	@property
	def MAKHZUUM(self):
		if not self.ARABIC:
			return "maḫzūm"
		else:
			return "مخزوم"
			
	@property
	def MURAFFAL(self):
		if not self.ARABIC:
			return "muraffal"
		else:
			return "مرفل"
			
	@property
	def MUDHAAL(self):
		if not self.ARABIC:
			return "muḏāl"
		else:
			return "مذال"
			
	@property
	def MUSABBAGH(self):
		if not self.ARABIC:
			return "musabbaġ"
		else:
			return "مسبغ"
			
	@property
	def MAHDHUUF(self):
		if not self.ARABIC:
			return "maḥḏūf"
		else:
			return "محذوف"
			
	@property
	def MAQTUUF(self):
		if not self.ARABIC:
			return "maqṭūf"
		else:
			return "مقطوف"
			
	@property
	def MAQSUUR(self):
		if not self.ARABIC:
			return "maqṣūr"
		else:
			return "مقصور"
			
	@property
	def MAQTUUC(self):
		if not self.ARABIC:
			return "maqṭūʿ"
		else:
			return "مقطوع"
			
	@property
	def MUSHACCATH(self):
		if not self.ARABIC:
			return "mušaʿʿaṯ"
		else:
			return "مشعث"
			
	@property
	def AHADHDH(self):
		if not self.ARABIC:
			return "aḥaḏḏ"
		else:
			return "أحذّ"
			
	@property
	def ASLAM(self):
		if not self.ARABIC:
			return "aṣlam"
		else:
			return "أصلم"
			
	@property
	def MAKSHUUF(self):
		if not self.ARABIC:
			return "makšūf"
		else:
			return "مكشوف"
			
	@property
	def MAWQUUF(self):
		if not self.ARABIC:
			return "mawqūf"
		else:
			return "موقوف"
			
	@property
	def ABTAR(self):
		if not self.ARABIC:
			return "abtar"
		else:
			return "أبتر"

	def get_saalim_adjective(self, foot: int) -> str:
		return self.SAALIM

	def get_kharm_cilla_adjective(self, foot: int, cilla: int) -> str:
		if foot == self.feet_enum.MUFAACALATUN:
			return self.MACDUUB
		else:
			return self.ATHLAM

	def _get_cilla_adjective(self, cilla: int) -> str:
		if cilla == self.cillas_enum.KHAZM:
			return self.MAKHZUUM
		elif cilla == self.cillas_enum.TARFIIL:
			return self.MURAFFAL
		elif cilla == self.cillas_enum.TADHYIIL:
			return self.MUDHAYYAL
		elif cilla == self.cillas_enum.TASBIIGH:
			return self.MUSABBAGH
		elif cilla == self.cillas_enum.HADHF:
			return self.MAHDHUUF
		elif cilla == self.cillas_enum.QATF:
			return self.MAQTUUF
		elif cilla == self.cillas_enum.QASR:
			return self.MAQSUUR
		elif cilla == self.cillas_enum.QATC:
			return self.MAQTUUC
		elif cilla == self.cillas_enum.TASHCIITH:
			return self.MUSHACCATH
		elif cilla == self.cillas_enum.HADHADH:
			return self.AHADHDH
		elif cilla == self.cillas_enum.SALM:
			return self.ASLAM
		elif cilla == self.cillas_enum.KASHF:
			return self.MAKSHUUF
		elif cilla == self.cillas_enum.WAQF:
			return self.MAWQUUF
		elif cilla == self.cillas_enum.BATR:
			return self.ABTAR
		else:
			raise RuntimeError("Unrecognized ʿilla: %d"%cilla)
	
	def get_cilla_adjective(self, foot: int, cilla: int) -> str:
		if cilla == self.cillas_enum.KHARM:
			return self.get_kharm_cilla_adjective(foot, cilla)
		else:
			return self._get_cilla_adjective(cilla)
			
	@property
	def THARM(self):
		if not self.ARABIC:
			return "ṯarm"
		else:
			return "ثرم"
			
	@property
	def SHATR(self):
		if not self.ARABIC:
			return "šatr"
		else:
			return "شتر"
			
	@property
	def KHARAB(self):
		if not self.ARABIC:
			return "ḫarab"
		else:
			return "خرب"
			
	@property
	def QASM(self):
		if not self.ARABIC:
			return "qaṣm"
		else:
			return "قصم"
			
	@property
	def JAMAM(self):
		if not self.ARABIC:
			return "ǧamam"
		else:
			return "جمم"
			
	@property
	def CAQS(self):
		if not self.ARABIC:
			return "ʿaqṣ"
		else:
			return "عقص"
			
	def get_kharm_zihaafa_adjective(self, cilla_adjective: str, foot: int, zihaafa: int):
		if zihaafa == self.zihaafas_enum.QABD:
			if foot == self.feet_enum.FACUULUN:
				return self.THARM
			elif foot == self.feet_enum.MAFAACIILUN:
				return self.SHATR
		elif zihaafa == self.zihaafas_enum.KAFF:
			if foot == self.feet_enum.MAFAACIILUN:
				return self.KHARAB
		elif zihaafa == self.zihaafas_enum.CASB:
			return self.QASM
		elif zihaafa == self.zihaafas_enum.CAQL:
			return self.JAMAM
		elif zihaafa == self.zihaafas_enum.NAQS:
			return self.CAQS
		else:
			return cilla_adjective + " " + self._get_zihaafa_adjective(zihaafa)
			
	@property
	def MAKHBUUL(self):
		if not self.ARABIC:
			return "maḫbūl"
		else:
			return "مخبول"
			
	@property
	def MAKHZUUL(self):
		if not self.ARABIC:
			return "maḫzūl"
		else:
			return "مخزول"
			
	@property
	def MASHKUUL(self):
		if not self.ARABIC:
			return "maškūl"
		else:
			return "مشكول"
			
	@property
	def MANQUUS(self):
		if not self.ARABIC:
			return "manqūṣ"
		else:
			return "منقوص"
			
	@property
	def MAKHBUUN(self):
		if not self.ARABIC:
			return "maḫbūn"
		else:
			return "مخبون"
			
	@property
	def MAWQUUS(self):
		if not self.ARABIC:
			return "موقوص"
		else:
			return ""
			
	@property
	def MUDMAR(self):
		if not self.ARABIC:
			return "muḍmar"
		else:
			return "مضمر"
			
	@property
	def MATWII(self):
		if not self.ARABIC:
			return "maṭwī"
		else:
			return "مطوي"
			
	@property
	def MAQBUUD(self):
		if not self.ARABIC:
			return "maqbūḍ"
		else:
			return "مقبوض"
			
	@property
	def MACQUUL(self):
		if not self.ARABIC:
			return "maʿqūl"
		else:
			return "معقول"
			
	@property
	def MACSUUB(self):
		if not self.ARABIC:
			return "maʿṣūb"
		else:
			return "معصوب"
			
	@property
	def MAKFUUF(self):
		if not self.ARABIC:
			return "makfūf"
		else:
			return "مكفوف"

	def _get_zihaafa_adjective(self, zihaafa: int) -> str:
		if zihaafa == self.zihaafas_enum.KHABL:
			return self.MAKHBUUL
		elif zihaafa == self.zihaafas_enum.KHAZL:
			return self.MAKHZUUL
		elif zihaafa == self.zihaafas_enum.SHAKL:
			return self.MASHKUUL
		elif zihaafa == self.zihaafas_enum.NAQS:
			return self.MANQUUS
		elif zihaafa == self.zihaafas_enum.KHABN:
			return self.MAKHBUUN
		elif zihaafa == self.zihaafas_enum.WAQS:
			return self.MAWQUUS
		elif zihaafa == self.zihaafas_enum.IDMAAR:
			return self.MUDMAR
		elif zihaafa == self.zihaafas_enum.TAYY:
			return self.MATWII
		elif zihaafa == self.zihaafas_enum.QABD:
			return self.MAQBUUD
		elif zihaafa == self.zihaafas_enum.CAQL:
			return self.MACQUUL
		elif zihaafa == self.zihaafas_enum.CASB:
			return self.MACSUUB
		elif zihaafa == self.zihaafas_enum.KAFF:
			return self.MAKFUUF

			
	def add_zihaafa_adjective(self, cilla_adjective: str, foot: int, cilla: int, zihaafa: int):
		if cilla == self.cillas_enum.KHARM:
			return self.get_kharm_zihaafa_adjective(cilla_adjective, foot, zihaafa)
		else:
			if zihaafa == self.zihaafas_enum.NOTHING:
				return cilla_adjective
			else:
				return cilla_adjective + " " + self._get_zihaafa_adjective(zihaafa)
	
	def get_adjective(self, foot: int, cilla: int, zihaafa: int):
		if cilla == self.cillas_enum.NOTHING and zihaafa == self.zihaafas_enum.NOTHING:
			return self.get_saalim_adjective(foot)
		
		elif cilla == self.cillas_enum.NOTHING:
			return self._get_zihaafa_adjective(zihaafa)
		
		else:
			cilla_adjective = self.get_cilla_adjective(foot, cilla)
			complete_adjective = self.add_zihaafa_adjective(cilla_adjective, foot, cilla, zihaafa)	
			return complete_adjective
