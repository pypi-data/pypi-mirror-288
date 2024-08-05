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
from cruscopoetry.core.renderers.htmlrenderer.metadata_renderer import HtmlMetadataRenderer
from cruscopoetry.core.jsonparser import JsonMetadata, JsonTranslations
from ..common.metric_elements import MetricElements
from typing import Tuple


class CruscoArudMetadataRenderer(HtmlMetadataRenderer):
	"""CruscoArud's renderer class of metadata. It acts as :class:`HtmlMetadataRenderer`, with the only difference that informations about metre and form of the poem are also represented here."""
	
	def __init__(self, metadata: JsonMetadata, translations: JsonTranslations, metre_name: str, form_name: str):
		super().__init__(metadata, translations)
		self.add_row("metre and form", "%s %s"%(metre_name, form_name))

	def render(self, translation_id: str) -> str:
		"""Organizes the metadata in a string as tabular format.
		
		Returns
			view (str): the view of the text as string.
		"""
		return super().render(translation_id)
