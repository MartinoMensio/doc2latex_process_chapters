# Doc2latex utility tool

This tool, given a Google Doc exported to latex using https://www.docx2latex.com/, cleans up the content and produces the chapter files (and abstract) that can be loaded in another latex template.

To make this work

- ensure to use Google Docs hierarchical headings, and for the abstract write it between the title ( preceeded by the underlined `Abstract` line) and before the first heading
- use Doc2Latex https://www.docx2latex.com/docx2latex_free
- extract the `.zip` file in the subdirectory `source`
- run the python script
- chech the output results in the folder `out`

The results are:

- `media` folder with all the pictures from the Google Doc. You may want to substitute them with vectorial pdfs
- `partials` folder that will contain the abstract and the chapters

## Note

This code is potentially full of bugs
