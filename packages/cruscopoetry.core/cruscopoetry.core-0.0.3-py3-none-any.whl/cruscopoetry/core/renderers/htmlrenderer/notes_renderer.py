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
from .utils import HtmlNode, TextNode
from ..abstractrenderer import AbstractNotesRenderer, AbstractNoteRenderer
from ...jsonparser import JsonNotes, JsonNote, JsonTranslations


class HtmlNoteRenderer(AbstractNoteRenderer):

	def __init__(self, number: str, text: str):
		super().__init__(number, text)
	
	def _make_link(self, reference: int):
		if reference == 0:
			return "#" + "text_table"
		else:
			return "#line_" + str(reference)
		
	def render(self):

		reference_node = HtmlNode("a", {"href": self._make_link(self.reference)}, TextNode(self.ref_string))
		reference_cell = HtmlNode("td", {"class": "reference"}, reference_node)

		text_cell = HtmlNode("td", {"class": "text"}, self.text)

		note_row = HtmlNode("tr", {"class": "note"}, [reference_cell, text_cell])
		return note_row


class HtmlNotesRenderer(AbstractNotesRenderer):

	NOTE_RENDERER_CLASS = HtmlNoteRenderer

	def __init__(self, jnotes: JsonNotes, lines_map: dict, jtranslations: JsonTranslations):
		super().__init__(jnotes, lines_map, jtranslations)
		
	def render(self, translation_id: str):
		notes_renderers = super().render(translation_id)
		
		section_div = HtmlNode("div", {"id": "notes_section"})
		title = HtmlNode("h1", {"id": "notes_title"}, "Notes")
		section_div.append(title)
		table = HtmlNode("table", {"id": "notes_table"})
		section_div.append(table)
		notes = [note.render() for note in notes_renderers]
		table.extend(notes)
		return section_div
		
		
		
		
		
		
		
		
		
		
		

