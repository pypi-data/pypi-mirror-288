CruscoPoetry Syntax: source texts
=================================

This document describes the syntax of the files containing the *text of a poem in its original language* that are to be parsed for building a CruscoPoetry Json File. 
From here on, such file will be referred to as ``STF`` (source text file).

This file is is a simple plain-text file (.txt), directly editable by the user. It followes in a tree-structured format. The first branches are the **sections**.

Sections
--------

Each ``STF`` is composed of three sections, each one containing different types of contents in a different format. These sections are:

:metadata:
    contains information about the poem's title, author, language, script (if transcribed from a written source). other custom information can be added in key-value format.
:text:
    contains the actual text
:notes:
    contains the text notes, which normally appear in renderings as end-notes.


Each section is composed of a **head** and a **body**. The head consists in a single line containing only the name of the section, written in UPPERCASE. In the next lines the body follows, each body 
following specific formatting rules. A section's body ends with the beginning of a new section or with the end of the file. Therefore, the normal aspect of a STF would be:

::

    optional lines before the first section, METADATA. The content of these lines 
    will not be included in the JSON file

    METADATA
    #here above the head of the metadata section. Here below follows the metadata body.
    #comments can be wrote inside the section body, but **not on the same line of a section head**.
    #comments are only one-line and are started by the # character.
    *<metadata body>*

    TEXT


    #here comes the text body. Sections body can start one or more lines after the section head,
    #and can end with one or more blank lines.
    *<text body>*

    NOTES

    #finally, here comes the notes body.
    *<notes_body>*

A section is said to be *empty* if only is head occurs in the file, *missing* if neither its head nor its body are there. TEXT and NOTES section can be empty or missing; METADATA can be neither
empty nor missing.

It is time to look at how the bodies of each section are formatted.

The Metadata section
--------------------

The body of the metadata section represents several pieces of information, called **fields**, that are organised as **key-value pairs**. Each pair occupies a single line and follows this syntax:

::

    key = value #comment if needed. Be it with or without this comment, this is a valid field

Both key and value of a field will be loaded in the Json file as strings. It is not possible to encode other types of data, such as numbers, booleans or the null value. Empty strings are not allowed as well.
There are **five mandatory fields** that need to be included, otherwise the building will crash. They are:

:title:
    Title of the composition

:author:
    Author of the composition.

:language:
    The language of the composition, in ISO 639-3 language code (case unsensitive)

:script:
    The script of the composition, in ISO 15924 code (case unsensitive)

:country:
    The country where the composition has been documented, in ISO 3166-1 alpha-3 code (case unsensitive)

Omitting one of these fields or inserting an invalid code when required will cause the building to crash.

Other additional fields can be introduced from the user with custom keys and values. Here comes an example:

::

    METADATA
    title = Solo et pensoso i più deserti campi
    
    author = Francesco Petrarca #fields can be separated by one or more blank lines
    language = ita  #Italian language
    country = fra   #composed in France
    script = latn   #Latin script
    #here custom fields follow
    
    form = sonnet
    metre = endecasillabo

The order of insertion of the fields (be they mandatory or not) is not relevant.

The Text section
----------------


In the Text section, the body of a poem is considered structured hierarchically in Stanzas, Lines and Cola (hemistichs). Two stanzas are separated by two or more new-line characters (that is, one or more blacnk lines); two lines of the same stanza are separated by one new line char. Here comes an example:

::

    TEXT
    Solo et pensoso i più deserti campi     #stanza 1, line 1
    vo mesurando a passi tardi et lenti,    #stanza 1, line 2
    et gli occhi porto per fuggire intenti  #stanza 1, line 3
    ove vestigio human l’arena stampi.      #stanza 1, line 4

    Altro schermo non trovo che mi scampi   #stanza 2, line 1
    dal manifesto accorger de le genti,     #stanza 2, line 2
    perché negli atti d’alegrezza spenti    #stanza 2, line 3
    di fuor si legge com’io dentro avampi:  #stanza 2, line 4


    #the number of blank lines between two
    #stanzas is indifferent, while greater than one



    sì ch’io mi credo omai che monti et piagge  #stanza 3, line 1
    et fiumi et selve sappian di che tempre     #stanza 3, line 2
    sia la mia vita, ch’è celata altrui.        #stanza 3, line 3
    #a single blank line occupied by a comment will still be considered as a stanza separator
    Ma pur sì aspre vie né sì selvagge          #stanza 4, line 1
    cercar non so ch’Amor non venga sempre      #stanza 4, line 2
    ragionando con meco, et io co·llui.         #stanza 4, line 1


Formatting the line
+++++++++++++++++++

In the transcription of the line there are some special characters with a syntactic function. They are two: the **label marker** and the **cola delimiters**

====== ======================================== =========================================================================================================================================================
Symbol Name                                     Description
====== ======================================== =========================================================================================================================================================
$      line label                               Assigns a **label**, i.e. a string identifier, to the line. The label string starts after this symbol and ends before the first whitespace character.
                                                It can contain alphanumeric characters and the underscore. The label is not a mandatory element in line formatting, but can be useful for referring to 
                                                the line during other functions (i.e. translations or notes referencing)
------ ---------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------
&      word-external colon delimiter (``WECD``) Represents a caesura, i.e. a boundary between two cola or hemistichs. This caesura, moreover, falls between two words.
§      word-internal colon delimiter (``WICD``) Same as  (``WECD``), but in this case it is marked that caesura splits a word internally
====== ======================================== =========================================================================================================================================================

Quick examples of the employment of these symbols:

::

    $line_with_WECD Hwæt. We Gardena & in geardagum #Beowulf, l. 1
    $line_with_WICD aʿnī faʿūlun wa-mafāʿīlun mufā §    ʿalatuni_ʿdud fā ʿi lātun qad qafā #Mubayyinu al-Iškāl by Majaxate Kala, l. 29

Notice that the two alphanumeric sequences immediately before and after ``WICD`` will be considered an only word, even if the ``WICD`` symbol itself is surreounded by whitespaces.

Formatting the colon
++++++++++++++++++++

A colon is considered as a sequences of words, each one delimitated by a space character. Other characters, for example those for punctuation, can naturally occur, but they will be ignored in further parsing steps (es. syllabification).

The following syntaxes apply only **within one colon** and can not be employed across colon-boundaries.

While parsing a colon, CruscoPoetry employs the functions coded in a language-relative package (``LRP``). ``LRP`` s are other packages belonging to the CruscoPoetry library, which take care ot tasks, such as syllabification and phoneme parsing, which are language specific. After having parsed the metadata section, cruscopoetry looks if a ``LRP`` corresponding to the give isocode exists. If it doesn't find it, the parsing ends at word-level; otherwise, it continues to syllables and phonemes. The syntax expressions outlined here below allows an optimal use of ``LRP`` s while parsing the text.

Manual syllabification
**********************

``[syl|la|bi|fied]``

During text parsing, syllabification is normally carried out by the ``LRP``. However, it can be useful in some cases to give manually the correct syllabification of a word. This is done enclosing the word in square brackets and using the pipe character **|** as syllable-boundary marker.

    ``It's not [tran|sal|pine|], it's [trans|al|pine]``

Alternate orthography
*********************

``<how it reads|how it sounds>``

While parsing syllables and phonemes, CruscoPoetry relies on the orthography rules contained in the ``LRP``. These include also the characters that can appear in the colon and need to be considered as graphemes. Sometimes, however, a colon can contain also other characers, for example in correspondende of foreign words. When the parser finds such characters, they print a warning and skip it. 
Therefore, the sentence:

    ``In Paris one reads everywhere “hôtel”``

would be parsed as if it were:

    ``In Paris one reads everywhere htel``

The ``ô`` character being skipped (notice that quotation marks are skipped as well). 
Many times, however, skipping the foreign character is not without consequences: the word ``htel`` would syllabify in a totally different manner than *hôtel*. In some languages, this can bring to fatal errors and make the building crash. To avoid this, one can indicate to the LRP to consider that word in an *alternate orthography*:

    ``In Paris one reads everywhere <hôtel|hôtel>``

The version of the word contained between ``<`` and ``|`` will be showed in renderings, and that between ``|`` and ``>`` will be used for further parsing. In this way, the problems derived from the ``ô`` character are avoided.

One can use alternate orthography also in conjunction with manual syllabification, but exclusively after the alternate orthograhy pipeline:

    ``In Paris one reads everywhere <hôtel|[ho|tel]>``

Notice that a pipeline character outside manual syllabification or alternate orthography expressions raises an error.

The Notes section
-----------------

It is composed of several notes, each one separated by **at least two newline characers**, that is, at least one blank line.
Each note is composed by three elements: a label (optional), a reference and the text:

::

    $note1_label (note1_reference) note1 text,
    which is multilane and ends with the blank line #or EOF, just to put a comment

    (note2_reference) note2 text #note that label is optional

Note labels follow the same rules of line labels (see `Formatting the line`_). Note texts are normal multiline strings. Some attention must instead be given to **note references**. A note can refer to the text as a whole or to a single line of it. There are three types of reference:

:all:
    The note refers to the whole text, and correspond to the word ``all``. 

:numeric:
    The note refers to a single line identified by its progressive number. The first line is 1 and the numeration continues up to the end of the poem, without looking at stanza boundaries.

:by label:
    A label of the line is given as reference. The referenced label must be preceded by the ``$`` character.

An example:

::

    METADATA
    title = Beowulf,
    author = unknown,
    language = ang #ancient English
    country = gbr
    script = latn

    TEXT

    Hwæt! Wé Gárdena & in géardagum
    $theodcyninga þéodcyninga & þrym gefrúnon·
    hú ðá æþelingas & ellen fremedon.

    NOTES

    &note_on_hwæt (1) The beginning with a one-syllable word, #this is a numeric reference to the first line. Of course, this comment will not be included within the note text.
    immediately followed by a period, is still today a prosodic wonder.

    ($theodcyninga) “þéod” means people, nation; “cyning” means king #reference by label. If the label is not in the text body, an error is raised. Same result if the label is not preceded by $

    (all) What a wonderful poem! #reference to the whole text