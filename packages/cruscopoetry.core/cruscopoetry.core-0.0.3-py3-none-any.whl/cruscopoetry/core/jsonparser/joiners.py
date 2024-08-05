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
import os


class Joiners:
	"""Stores the character that are used to join together portions of text fom the json file, if this has be represented as plain text"""

	WORDS = " "
	COLA = " & "
	WORD_INTERNAL_COLA = " § "
	COLA_TRANSCRIPTION = " · "
	WORD_INTERNAL_COLA_TRANSCRIPTION = "·"
	LINES = os.linesep
	STANZAS = os.linesep*2
	NOTES = " & "
	METADATA_FIELDS_INTERNAL = " = "
	METADATA_FIELDS = os.linesep

