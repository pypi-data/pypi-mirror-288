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
from .line_renderer import CruscoArudHtmlLineRenderer
from .disposers import CruscoArudHtmlNoTranslationDisposer, CruscoArudHtmlAfterTextDisposer, CruscoArudHtmlEachStanzaDisposer, CruscoArudHtmlEachLineDisposer
from cruscopoetry.core.renderers.htmlrenderer.utils import HtmlElement, NullNode, TextNode, HtmlNode
from cruscopoetry.core.renderers.htmlrenderer.text_body_renderer import HtmlTextBodyRenderer
from cruscopoetry.core.renderers import TranslationArrangement
from cruscopoetry.core.jsonparser import JsonLine, JsonText
from typing import Tuple


class CruscoArudTextBodyRenderer(HtmlTextBodyRenderer):

	LINE_RENDERER_CLASS = CruscoArudHtmlLineRenderer

	NO_TRANSLATION_DISPOSER = CruscoArudHtmlNoTranslationDisposer
	AFTER_TEXT_TRANSLATION_DISPOSER = CruscoArudHtmlAfterTextDisposer
	EACH_STANZA_TRANSLATION_DISPOSER = CruscoArudHtmlEachStanzaDisposer
	EACH_LINE_TRANSLATION_DISPOSER = CruscoArudHtmlEachLineDisposer

	def __init__(self, json_text: JsonText, plugin_data: dict, feet_sequence: Tuple[int, ...], elements: MetricElements = None):
		super().__init__(json_text)
		self._elements = elements
		self._plugin_data = plugin_data
		self._feet_sequence = feet_sequence

	def build_line_renderer(self, jline: JsonLine, translation_id: str) -> CruscoArudHtmlLineRenderer:
		line_parsing = self._plugin_data[jline.index_in_poem]
		return self.__class__.LINE_RENDERER_CLASS(jline, translation_id, line_parsing, self._feet_sequence, self._elements)

	def build_disposer(self, line_renderers : Tuple[Tuple[CruscoArudHtmlLineRenderer]], translation_arrangement: TranslationArrangement):
		return super().build_disposer(line_renderers, translation_arrangement)

	def render(self, translation_id: str, translation_arrangement: TranslationArrangement, line_numbers_after: int) -> str:
		body_wrapper = super().render(translation_id, translation_arrangement, line_numbers_after)
		return body_wrapper
