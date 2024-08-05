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
import abc
from ...jsonparser import JsonNotes, JsonNote
from typing import Tuple


class AbstractNoteRenderer(metaclass=abc.ABCMeta):
	"""Abstract class for the rendering of a single note of a CruscoPoetry JSON file.
	
	Args:
		reference (int): the number of the poem's line the note is referenced to (or 0 if it is referenced to all the verses)
		lines_map (str): the note's text.
	
	Attrs:
		reference (int): the number of the poem's line the note is referenced to (or 0 if it is referenced to all the verses)
		lines_map (str): the note's text.
	"""
	
	ALL_LABEL = "*"

	def __init__(self, reference: int, text: str):
		self._reference = reference
		self._text = text

	@property
	def reference(self):
		return self._reference
	
	@property
	def text(self):
		return self._text
		
	@property
	def ref_string(self) -> str:
		"""Returns a string representing the note's reference."""
		if self.reference == 0:
			return self.__class__.ALL_LABEL
		else:
			return str(self.reference)
	
	@abc.abstractmethod
	def render(self) -> str:
		return "%s: %s"%(self.ref_string, self.text)
	

class AbstractNotesRenderer(metaclass=abc.ABCMeta):
	"""Abstract class for the rendering of the notes of a CruscoPoetry JSON file.
	
	Args:
		jnotes (JsonNotes): the object representing the notes section of the json parsing of the poem
		lines_map (dict): a dict where every label that has been set for a line is associated to the correpsonding line number.
	
	Attrs:
		notes (Tuple[AbstractNoteRenderer]): the renderers of notes of the poem.
		
	This class has two abstract methods:
	 - build_note_renderer
	 - render
	
	Concrete implementations of this class can be easily built by setting the class argument NOTE_RENDERER_CLASS with the concrete implementation of AbstractNoteRenderer that one wants to use.
	
	While implemented the render method, calling it form super() will return a list of instances of NOTE_RENDERER_CLASS representing the notes to render.
	"""
	
	NOTE_RENDERER_CLASS = AbstractNoteRenderer

	def __init__(self, jnotes, lines_map, jtranslations):
		self._jnotes = jnotes
		self._lines_map = lines_map
		self._jtranslations = jtranslations
	
	@property
	def lines_map(self):
		return self._lines_map
	
	@property
	def jnotes(self):
		return self._jnotes
		
	@property
	def jtranslations(self):
		return self._jtranslations

	def _get_note_reference(self, note: JsonNote) -> int:
		"""If the parameter 'note' is referenced by verse number or by 'all', it returns the reference. If the note is referenced by a line label, it will return the line's number.
		Finally, if the reference is 'all', it returns 0.
		"""
		
		if note.reference.isdigit():
			return int(note.reference)
		elif note.reference == "all":
			return 0
		else:
			index = self.lines_map[note.reference]
			return index+1

	def build_source_note_renderer(self, note, translation_id: str):
		reference = self._get_note_reference(note)

		text = note.text if translation_id == None else note.get_translation_by_id(translation_id)
		return self.__class__.NOTE_RENDERER_CLASS(reference, text)
		
	def build_translation_notes_renderer(self, translation_id: str):
		translation = self.jtranslations.get_translation_by_id(translation_id)
		ret_list = []
		if translation != None:
			for note in translation.translation_notes:
				line_number = self._get_note_reference(note)
				ret_list.append(self.__class__.NOTE_RENDERER_CLASS(line_number, note.text))
		return ret_list
	
	@abc.abstractmethod
	def render(self, translation_id: str = None) -> str:
		"""Provides the renderings of the notes, ordered by the numbers of the lines they are referenced to.
		This abstract method returns a tuple of instances of the class stored in the static attribute NOTE_RENDERER_CLASS, each one representing a note to be renderer. Concrete implementation can
		get this tuple calling directly the super method; then they have to organize the renderings in a string form and return ìt.
		Args:
			translation_id (str): the id of the translation that should be included in the rendering, or None if the source text needs to be included.
		"""
		#first we build the renderers of the source notes:
		note_renderers = [self.build_source_note_renderer(note, translation_id) for note in self.jnotes.iter_notes()]

		#then we extend the list we the translation notes and sort all the items by reference:
		note_renderers.extend(self.build_translation_notes_renderer(translation_id))
		note_renderers = sorted(note_renderers, key = lambda note: note.reference)

		note_renderers = tuple(note_renderers)
		return note_renderers
