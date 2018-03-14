# Doc2latex utility tool

This tool, given a Google Doc exported to latex using https://www.docx2latex.com/, cleans up the content and produces the chapter files (and abstract) that can be loaded in another latex template.

To make this work, specific rules have to be used while writing the Google Docs document:

- ensure to use Google Docs hierarchical headings
- for the abstract write it between the title ( preceeded by the underlined `Abstract` line) and before the first heading
- footnotes to citations must be in the form `Key:<BIBITEM_KEY> <ANY_TEXT CAN FOLLOW>` where `<BIBITEM_KEY>` is the identifier of the bibitem.
- for images substitution, add a `[FIG:<figure_identifier> CAPTION:<caption to insert for the figure>]` and use refs like `[REF FIG:<figure_identifier>]` where `<figure_identifier>` is the name of the pdf file to be placed in the folder `figures`.
- for tables to be listed in TOC, use `[TABLE:<table_identifier> CAPTION:<Any text there>]`, that can be referenced with `[REF TABLE:<table_identifier>]`
- to have cross references use `[REF <LABEL>]` where `<LABEL>` has been used inside a declaration `[LABEL:<LABEL>]`

Procedure:

- use Doc2Latex https://www.docx2latex.com/docx2latex_free
- extract the `.zip` file in the subdirectory `source`
- run the python script
- chech the output results in the folder `out`

The results are:

- `media` folder with all the pictures from the Google Doc. You may want to substitute them with vectorial pdfs
- `partials` folder that will contain the abstract and the chapters

## Note

This code is potentially full of bugs
