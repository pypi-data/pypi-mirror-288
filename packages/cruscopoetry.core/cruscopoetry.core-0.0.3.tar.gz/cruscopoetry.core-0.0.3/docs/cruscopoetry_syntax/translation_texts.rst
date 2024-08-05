CruscoPoetry Syntax: translation texts
======================================

Translations texts have a similar syntax to source texts, but simplified in some aspects. For this reason, their syntax will be presented contrastively to that of Source Texts: the reader that doesn't know CruscoPoetry Source Text syntax can read `this page`_ .

.. _this page: `CruscoPoetry Source Text Syntax page`_

.. _CruscoPoetry Source Text Syntax page: https://gitlab.com/kikulacho92/cruscopoetry_new/-/blob/master/cruscopoetry_core/cruscopoetry_syntax/source_texts.rst?ref_type=heads

Sections
--------

There are **four sections**: ``METADATA``, ``TEXT``, ``SOURCE_NOTES`` and ``TRANSLATION_NOTES``. The sections are structured in the same way of source texts: a head consisting in the name of the section in uppercase, occupying one self-standing line that contains no other alphanumerical character, and a body with different formatting rules.

The Metadata Section
--------------------

It is similar to the homonym section of Source Texts, but the mandatory fields are different. There are only two:

:id:    A user-defined identifier string. This string will be used to refer to the translation in future operations (for example, to remove it from the CruscoPoetry Json File or to use it in a rendering). Suppose the case of a CruscoPoetry Json File which already contains a translation with a given id; if a user tries to add another translation with the same id, the new translation will overwrite the old one.

:language:  the language of the translation in ISO 639-3 code.


The Text Section
----------------

It has a simple structure than the correspondent one in Source Texts. The text is considered divided only in lines, by one or more newline-characters: division in stanzas is not considered. Therefore leaving 0, one or more blank lines between two verse lines brings no difference in the output.
Each line of the translation is considered the translated version of a line of the source text. A line in the translation file can be made point to a specific line in the source text in two ways:

 - **implicitly**, by its position. If a line is the nth one appearing in the text section of a translation file, it will be considered the translation of the n :sup:`th` line of the Source Text
 - **explicitly** by a reference. Be ``$mylabel`` the label of a line in the Source Text. Then a line of the Translation can be made point to that line of the Source Text with the following syntax:

::

    ($mylabel) the translation of this line

The Source Notes Section
------------------------

This section contains the translation of the notes contained in the ``NOTES`` section of the Source Text file. Each note translation is separated by two or more newline-characters, that is, at least one blank line. Like the lines, a note translation can point to a specific note in the source text **implicitly**, by its index, or **explicitly**, by a reference. For example:

::

    SOURCE_NOTES
    Note text, which
    can be multiline. This note is the first in the section and point then to the first note of the source text

    ($thatimportantnote) This note points to the note in the source text presenting the label $thatimportantnote.

The Translation Notes Section
-----------------------------

This section contains the notes that are specific of a translation and do not correspond to other notes in the Source Text file. Like Source Notes, they contain multiline text and are separated by one or more blank lines. But Translation Notes follow a different syntax than source notes:

 - they **do not support implicit reference**. A reference then must always be specified.
 - references work as those of **notes of the source text**. To resume here:

    ============== ================================== ============================================================================================================
    Reference type Syntax                             Meaning
    ============== ================================== ============================================================================================================
    Numeric        ``(n)``, where ``n`` is an integer The note refers to the n :sup:`th` line in the source text
    By label       ``($mylabel)``                     The note refers to the line in the source text labelled as ``$mylabel``
    General        ``(all)``                          The note refers to the whole text.
    ============== ================================== ============================================================================================================
