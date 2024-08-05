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
from ..common.metric_elements import MetricElements
from ..common.elements.feet import Foot
from cruscopoetry.core.jsonparser import JsonLine, JsonColon
from cruscopoetry.core.renderers.htmlrenderer.utils import HtmlElement, NullNode, TextNode, HtmlNode
from cruscopoetry.core.renderers.abstractrenderer import AbstractLineRenderer
from cruscopoetry.core.renderers.htmlrenderer.line_renderer import HtmlLineRenderer, HtmlColonRenderer
from typing import List, Tuple


class FootRenderer:
	
	def __init__(self, foot: Foot, variation: int, elements: MetricElements = None):
		self._elements = elements if elements != None else MetricElements()
		self._foot = foot
		self._cilla = elements.cillas_pool[variation // self._elements.foot_info_base_16_order]
		self._zihaafa = elements.zihaafas_pool[variation % self._elements.foot_info_base_16_order]
		sequence = self._cilla.transform(foot)
		self.sequence = self._zihaafa.transform(sequence)

	@property
	def foot(self):
		return self._foot

	@property
	def cilla(self):
		return self._cilla

	@property
	def zihaafa(self):
		return self._zihaafa

	@property
	def count_syllables(self):
		return self.sequence.count("0")
		
	@property
	def foot_namer(self):
		return self._elements.foot_namer
		
	@property
	def elements_name(self):
		return (self.foot.name, self.cilla.name, self.zihaafa.name)
		
	@property
	def name(self):
		foot, cilla, zihaafa = int(self.foot), int(self.cilla), int(self.zihaafa)
		adjective = self.foot_namer.get_adjective(foot, cilla, zihaafa)
		
		return "%s %s"%(self.foot.name, adjective)


class CruscoArudColonRenderer(HtmlColonRenderer):
	
	def __init__(self, jcolon: JsonColon, colon_parsing: List[int], feet_sequence: Tuple[int], elements: MetricElements = None):
		super().__init__(jcolon)

		self._elements = elements if elements != None else MetricElements()

		_feet_sequence: Tuple[Foot] = tuple(elements.feet_pool[foot] for foot in feet_sequence)
#		variations_array = self._jcolon.jdict[self._elements.configuration.json_fields["COLA_FIELD_NAME"]]

		self.foot_renderers = tuple(FootRenderer(_feet_sequence[i], colon_parsing[i], elements) for i in range(len(_feet_sequence)))
	
	def _get_foot_syllables(self):
		feet_lengths = tuple(foot_renderer.count_syllables for foot_renderer in self.foot_renderers)
		syllables = [str(syllable) for syllable in self._jcolon.iter_syllables()]
		feet = []
		for i in range(len(feet_lengths)):
			feet.append(syllables[:feet_lengths[i]])
			syllables = syllables[feet_lengths[i]:]
		return feet
			
	def get_foot_names(self):
		return [foot.name for foot in self.foot_renderers]

	def render_feet_syllables_cells(self):
		feet = self._get_foot_syllables()
		feet = tuple(HtmlNode("td", {"class": "foot_text"}, " ".join(foot)) for foot in feet)
		return feet

	def render_feet_names_cells(self):
		names = self.get_foot_names()
		names = tuple(HtmlNode("td", {"class": "foot_name"}, name) for name in names)
		return names
	
	def render_source_cell(self):
		"""Renders the colon's source text in a td-tagged HtmlNode whose colspan equals the number of the colon's feet."""
		colspan = len(self.foot_renderers)
		cell = HtmlNode("td", {"colspan": str(colspan)}, self.transcription)
		return cell


class CruscoArudHtmlLineRenderer(HtmlLineRenderer):

	COLON_RENDERER = CruscoArudColonRenderer
	
	def __init__(self, jline: JsonLine, translation_id: str, line_parsing: List[List[int]], feet_sequence: Tuple[int, ...], elements: MetricElements = None):
		AbstractLineRenderer.__init__(self, jline, translation_id)

		half_index = len(feet_sequence) // 2
		self.sadr, self.cajz = feet_sequence[:half_index], feet_sequence[half_index:]
		self._elements = elements if elements != None else MetricElements()

		cola = []
		cola_number = self.count_cola()
		for i, jcolon in enumerate(self.jline.iter_cola()):
			if i < (cola_number-1):
				cola.append(self.build_colon(jcolon, line_parsing[i], self.sadr))
			else:
				cola.append(self.build_colon(jcolon, line_parsing[i], self.cajz))
		self.cola = tuple(cola)
	
	def build_colon(self, jcolon: JsonColon, colon_parsing, feet_sequence: Tuple[int, ...]):
		return self.__class__.COLON_RENDERER(jcolon, colon_parsing, feet_sequence, self._elements)
	
	def count_cola(self):
		return self._jline.count_cola()
	
	@property
	def colon_separator(self):
		return HtmlNode("td", {"class": "separator"}, super().colon_separator)
		
	def count_feet(self):
		ret_int = 0
		for colon in self.cola:
			ret_int += len(colon.foot_renderers)
		return ret_int

	def get_feet_syllables(self) -> Tuple[HtmlNode, ...]:
		feet_syllables = []
		for i, colon in enumerate(self.cola):
			if i > 0:
				feet_syllables.append(self.colon_separator)
			feet_syllables.extend(colon.render_feet_syllables_cells())
		return feet_syllables

	def get_feet_names(self):
		feet_names = []
		for i, colon in enumerate(self.cola):
			if i > 0:
				feet_names.append(self.colon_separator)
			feet_names.extend(colon.render_feet_names_cells())
		return feet_names


	def get_source(self) -> Tuple[HtmlNode]:
		cells = tuple(colon.render_source_cell() for colon in self.cola)
		cells = tuple(self.colon_separator.join(cells))
		return cells

	def get_translation(self) -> HtmlNode:
		translation = self.translation if self.translation != None else ''
		cell = HtmlNode("td", {"class": "translation", "colspan": str(self.count_feet())}, translation)
		return cell
