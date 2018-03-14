import os
import re
import subprocess

def main(only_vectorial_figures=False):
    '''only_vectorial_figures=False uses the ./source/media raster images
    
    only_vectorial_figures=True uses the vectorial figures placed in ./out/figures'''
    print('step 1: download from https://www.docx2latex.com/docx2latex_free the latex document extract and place it in the "./source" directory. Enter when ready')
    input()
    input_path = './source'
    output_path = './out/partials'
    subprocess.call(['rm', '-rf', './out/media/'])
    if not only_vectorial_figures:
        subprocess.call(['cp', '-r', './source/media/', './out/'])
    for filename in os.listdir(input_path):
        if re.match(r'.*\.tex', filename):
            print('found source file', filename)
            process_file(os.path.join(input_path, filename), output_path, only_vectorial_figures)

def process_file(file_path, output_path, only_vectorial_figures):
    with open(file_path) as f:
        file_content = f.read()
    
    file_content = re.search(r'\\begin{document}[\s\S]*\\uline{Abstract}\\par([\s\S]*)\\end{document}', file_content).groups()[0]

    file_content = re.sub(r'\\section{', '\\chapter{', file_content)
    file_content = re.sub(r'\\subsection{', '\\section{', file_content)
    file_content = re.sub(r'\\subsubsection{', '\\subsection{', file_content)
    file_content = re.sub(r'\\paragraph{', '\\subsubsection{', file_content)
    file_content = re.sub(r'\\subparagraph{', '\\paragraph{', file_content)
    # unrecognized characters
    file_content = re.sub(r'[’‘]', '\'', file_content)
    file_content = re.sub(r'[–—]', '-', file_content)
    file_content = re.sub(r'⋅', r'\\cdot ', file_content)
    file_content = re.sub(r'ĉ', r'\\hat c', file_content)
    # strange table error
    #file_content = re.sub('}}}}', '}}', file_content)
    #file_content = re.sub('}}}', '}}', file_content)
    # remove empty hrefs
    file_content = re.sub(r'\\href{}', '', file_content)
    # remove ugly vertical spaces
    file_content = re.sub(r'\\vspace{\\baselineskip}', '', file_content)
    # remove manual page breaks
    file_content = re.sub(r'\\newpage', '', file_content)


    # footnote to cite
    file_content = re.sub(r'\s*\\footnote{\s*Key:(\w*)\s[^}]*}', r'~\\cite{\1}', file_content)
    # build links from URLs
    file_content = re.sub(r'\\footnote{\s*(http\S+)\s*}', r'\\footnote{\\url{\1}}', file_content)

    # manual alignment of text
    file_content = re.sub(r'\\begin{FlushLeft}', '', file_content)
    file_content = re.sub(r'\\end{FlushLeft}', '', file_content)

    # table captions
    file_content = re.sub(r'\\end{table}[^[]*\[TABLE:(\S+) CAPTION:([^]]*)\]', r'\\caption{\2}\\label{tab:\1}\n\\end{table}', file_content)
    # add caption placeholder if no declared
    file_content = re.sub(r'\\end{tabular}\s*\\end{table}', r'\\end{tabular}\\caption{TABLE NAME}\n\\end{table}', file_content)
    file_content = re.sub(r'\s\[REF\sTABLE:(\S+)\]', r'~\\ref{tab:\1}', file_content)

    # add placeholder captions for figures, to show up in list of figures
    file_content = re.sub(r'\\end{figure}', r'\\caption{FIGURE NAME}\n\\end{figure}', file_content)

    # 1 remove figures
    #file_content = re.sub(r'\\begin{figure}([^%]*)\\end{figure}', '', file_content)
    # remove figures that have vectorial pdf
    file_content = re.sub(r'\\begin{figure}[^%]*\\end{figure}[^[]*\[FIG:(\S*)\sCAPTION:([^]]+)\]', r'\\begin{figure}[!htbp]\n    \\centering\n    \\includegraphics[width=\\linewidth]{figures/\1}\n    \\caption{\2}\label{fig:\1}\n\\end{figure}', file_content)
    # 3 ref to figures
    file_content = re.sub(r'\s\[REF\sFIG:([^]]+)\]', r'~\\ref{fig:\1}', file_content)

    # labels and ref management
    file_content = re.sub(r'\[LABEL:([^]]+)\]', r'\\label{\1}', file_content)
    file_content = re.sub(r'\[REF:([^]]+)\]', r'\\ref{\1}', file_content)
    

    # remove \par because paragraphs are already separated by empty lines
    file_content = re.sub(r'\\par(\s+)', r'\1', file_content)
    # remove empty lines
    file_content = re.sub(r'\n{3,}', r'\n\n', file_content)

    delimiter = '\\chapter{'
    partial_file_header = '% !TEX encoding = utf8\n% !TEX root = ../main.tex\n\n'
    partial_file_header += '% This content has been generated automatically from https://www.docx2latex.com/docx2latex_free and https://github.com/MartinoMensio/doc2latex_process_chapters \n'
    partial_file_header += '% Consider editing the source Google Doc instead of this one!\n\n\n'
    for i, c in enumerate(file_content.split('\\chapter{')):
        if i == 0:
            # abstract sections are not to be shown in Table Of Contents
            c = re.sub(r'\\section{([^}]*)}', r'\\section*{\1}', c)
            write_file('abstract.tex', partial_file_header + c, output_path)
        else:
            write_file('chapter_{}.tex'.format(i), partial_file_header + delimiter + c, output_path)

def write_file(file_name, content, output_path):
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, file_name), 'w') as f:
        f.write(content)


if __name__ == '__main__':
    main(only_vectorial_figures=False)