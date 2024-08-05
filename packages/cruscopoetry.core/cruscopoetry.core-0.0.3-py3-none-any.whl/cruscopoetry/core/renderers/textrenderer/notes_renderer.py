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
from .joiners import Joiners
from ..abstractrenderer import AbstractNotesRenderer, AbstractNoteRenderer
import os
from .joiners import Joiners


class NoteRenderer(AbstractNoteRenderer):

	def __init__(self, reference: int, text: str):
		super().__init__(reference, text)
		
	def render(self, indent):
		return indent + super().render()


class NotesRenderer(AbstractNotesRenderer):

	NOTE_RENDERER_CLASS = NoteRenderer

	def __init__(self, jnotes, lines_map, jtranslations):
		super().__init__(jnotes, lines_map, jtranslations)

	def render(self, translation_id: str, indent: str):
		note_renderers = super().render(translation_id)
		note_renderings = tuple(note_renderer.render(indent) for note_renderer in note_renderers)
		return Joiners.NOTE.join(note_renderings)
