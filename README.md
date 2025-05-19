# chapter_bibliography_maker
A command line tool that allows the automatic creation of chapter bibliographies from a master bibliography file.

## Example

The tool should be used in the following way. The chatper TeX file and the master bibliography file are provided as command line arguments.

```
python3 create_chapter_bibliographies.py -c chapter1.tex -m bibliography.bib
```

The tool will then scan the chapter TeX file for in-line references and pull them out of the master .bib file into a chapter .bib file named in the same way as the chapter TeX file.
The entries in the chapter bibliography will appear in the same order as they did in the master bibliography.

Alternatively, the following script can be called, which will order the entries in the chapter bibliography by the order that
the references to them appear in the chapter source.

```
python3 create_ordered_chapter_bibliographies.py -c chapter1.tex -m bibliography.bib
```
