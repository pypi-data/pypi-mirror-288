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
from cruscopoetry.core.jsonparser import JsonText, JsonTranslations, JsonTranslation, JsonStanza, JsonLine, JsonColon
from cruscopoetry.core.renderers.htmlrenderer.disposers import HtmlNoTranslationDisposer, HtmlAfterTextDisposer, HtmlEachStanzaDisposer, HtmlEachLineDisposer, HtmlDisposer
from cruscopoetry.core.renderers.htmlrenderer.utils import *
from typing import Tuple
from .line_renderer import CruscoArudHtmlLineRenderer


class CruscoArudHtmlDisposer(HtmlDisposer):
	
	def get_line_source_text(self, line: CruscoArudHtmlLineRenderer, line_numbers_after: int) -> Tuple[HtmlNode, HtmlNode]:
		"""Returns a row containing the line number cell if required, else a blank cell, and more cells each one with the transcription of one of the line's cola."""
		number_cell = self.get_number_cell(line.number, line_numbers_after)
		source_cells = (number_cell,) + line.get_source()
		source_row = HtmlNode("tr", {"id": "line_%d"%line.number,  "class": "line source"}, source_cells)
		return source_row
	
	def get_line_feet_syllables(self, line: CruscoArudHtmlLineRenderer, line_numbers_after: int) -> HtmlNode:
		syllables = line.get_feet_syllables()
		
		syllables_row = HtmlNode("tr", {"class": "line feet_syllables"})
		syllables_row.append(self.build_blank_cell())
		syllables_row.extend(syllables)
		return syllables_row
	
	def get_line_feet_names(self, line: CruscoArudHtmlLineRenderer, line_numbers_after: int) -> HtmlNode:
		feet_names = line.get_feet_names()
		feet_row = HtmlNode("tr", {"class": "line feet_names"})
		feet_row.append(self.build_blank_cell())
		feet_row.extend(feet_names)
		return feet_row

	def get_line_source(self, line: CruscoArudHtmlLineRenderer, line_numbers_after: int) -> Tuple[HtmlNode, HtmlNode, HtmlNode]:
		"""Returns two tuples of td-tagged HtmlNode instances, the first representing the line's number (or a blank cell) plus the line's syllables grouped in foot, the second a blank cell plus
		the line's feet names.
		
		Args:
			line (HtmlLineRenderer): the line whose source is needed
			line_numbers_after (int): if line.number % line_numbers_after == 0, then also the line number will be inserted in the rendering.
		
		Returns:
			syllables_row (HtmlNode): a tr-taggedHtmlNode containing the line's number (if needed, otherwise a blank cell) and the syllables grouped in feet
			feet_names_row (HtmlNode): a tr-taggedHtmlNode containing a blanl cell the names of the line's feet
		"""
		source_row = self.get_line_source_text(line, line_numbers_after)
		syllables_row = self.get_line_feet_syllables(line, line_numbers_after)
		feet_row = self.get_line_feet_names(line, line_numbers_after)

		return source_row, syllables_row, feet_row

	def get_stanza_source(self, stanza: Tuple[CruscoArudHtmlLineRenderer, ...], line_numbers_after: int) -> Tuple[HtmlNode, ...]:
		"""Returns the renderings of the source texts of the lines composing the stanza as a tuple of tr-tagged HtmlNode instances"""

		stanza_rendering = []
		for i, line in enumerate(stanza):
			if i > 0:
				stanza_rendering.append(self.build_blank_row())
			stanza_rendering.extend(self.get_line_source(line, line_numbers_after))
		return tuple(stanza_rendering)

	def get_text_source(self, line_renderers: Tuple[Tuple[CruscoArudHtmlLineRenderer, ...]], line_numbers_after) -> Tuple[HtmlNode, ...]:
		"""Returns the renderings of the source texts of the lines composing the text as a tuple of tr-tagged HtmlNode instances"""

		stanza_renderings = tuple(self.get_stanza_source(stanza, line_numbers_after) for stanza in line_renderers)
		text_rendering = []
		for i, stanza in enumerate(stanza_renderings):
			if i > 0:
				for j in range(2):
					text_rendering.append(self.build_blank_row())
			text_rendering.extend(stanza)
		return text_rendering


class CruscoArudHtmlNoTranslationDisposer(HtmlNoTranslationDisposer):

	UTILITIES = CruscoArudHtmlDisposer()

	def __init__(self, line_renderers: Tuple[Tuple[CruscoArudHtmlLineRenderer, ...]]):
		super().__init__(line_renderers)

	def get_rendered_lines(self, line_numbers_after: int):
		source_text = self.utilities.get_text_source(self.line_renderers, line_numbers_after)
		text_table = self.utilities.build_text_table()
		text_table.extend(source_text)		
		return text_table


class CruscoArudHtmlAfterTextDisposer(HtmlAfterTextDisposer):

	UTILITIES = CruscoArudHtmlDisposer()

	def __init__(self, line_renderers: Tuple[Tuple[CruscoArudHtmlLineRenderer, ...]]):
		super().__init__(line_renderers)

	def get_rendered_lines(self, line_numbers_after: int):
		return super().get_rendered_lines(line_numbers_after)


class CruscoArudHtmlEachStanzaDisposer(HtmlEachStanzaDisposer):

	UTILITIES = CruscoArudHtmlDisposer()

	def __init__(self, line_renderers: Tuple[Tuple[CruscoArudHtmlLineRenderer, ...]]):
		super().__init__(line_renderers)

	def get_rendered_stanza(self, stanza: Tuple[CruscoArudHtmlLineRenderer, ...], line_numbers_after: int):
		source_stanza = self.utilities.get_stanza_source(stanza, line_numbers_after)
		translation_stanza = self.utilities.get_stanza_translation(stanza, line_numbers_after)
		
		stanza_rendering = []
		stanza_rendering.extend(source_stanza)
		for i in range(2):
			stanza_rendering.append(self.utilities.build_blank_row())
		stanza_rendering.extend(translation_stanza)
		return stanza_rendering

	def get_rendered_lines(self, line_numbers_after: int):
		stanza_renderings = tuple(self.get_rendered_stanza(stanza, line_numbers_after) for stanza in self.line_renderers)
		text_table = self.utilities.build_text_table()
		
		for i, stanza in enumerate(stanza_renderings):
			if i > 0:
				for j in range(3):
					text_table.append(self.utilities.build_blank_row())
			text_table.extend(stanza)
		
		return text_table
		

class CruscoArudHtmlEachLineDisposer(HtmlEachLineDisposer):

	UTILITIES = CruscoArudHtmlDisposer()

	def __init__(self, line_renderers: Tuple[Tuple[CruscoArudHtmlLineRenderer, ...]]):
		super().__init__(line_renderers)

	def get_rendered_line(self, line: CruscoArudHtmlLineRenderer, line_numbers_after: int):
		source_line = self.utilities.get_line_source(line, line_numbers_after)
		#since the translation is immediately after the source text, there is no need to include the line number even at its row, so we pass None as number_after argument:
		translation_line = self.utilities.get_line_translation(line, None)
		
		line_rendering = []
		line_rendering.extend(source_line)
		for i in range(2):
			line_rendering.append(self.utilities.build_blank_row())
		line_rendering.append(translation_line)
		return tuple(line_rendering)

	def get_rendered_stanza(self, stanza: Tuple[CruscoArudHtmlLineRenderer, ...], line_numbers_after: int):
		line_renderings = tuple(self.get_rendered_line(line, line_numbers_after) for line in stanza)
		stanza_rendering = []
		for i, line in enumerate(line_renderings):
			if i > 0:
				for j in range(3):
					stanza_rendering.append(self.utilities.build_blank_row())
			stanza_rendering.extend(line)
		return tuple(stanza_rendering)

	def get_rendered_lines(self, line_numbers_after: int):
		stanza_renderings = tuple(self.get_rendered_stanza(stanza, line_numbers_after) for stanza in self.line_renderers)
		text_table = self.utilities.build_text_table()
		
		for i, stanza in enumerate(stanza_renderings):
			if i > 0:
				for j in range(4):
					text_table.append(self.utilities.build_blank_row())
			text_table.extend(stanza)
		
		return text_table
