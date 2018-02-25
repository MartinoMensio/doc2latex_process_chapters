import os
import re
import subprocess

def main():
    print('step 1: download from https://www.docx2latex.com/docx2latex_free the latex document extract and place it in the "./source" directory. Enter when ready')
    input()
    input_path = './source'
    output_path = './out/partials'
    subprocess.call(['cp', '-r', './source/media/', './out/'])
    for filename in os.listdir(input_path):
        if re.match(r'.*\.tex', filename):
            print('found source file', filename)
            process_file(os.path.join(input_path, filename), output_path)

def process_file(file_path, output_path):
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
    # strange table error
    #file_content = re.sub('}}}}', '}}', file_content)
    #file_content = re.sub('}}}', '}}', file_content)
    # remove empty hrefs
    file_content = re.sub(r'\\href{}', '', file_content)
    # remove ugly vertical spaces
    file_content = re.sub(r'\\vspace{\\baselineskip}', '', file_content)
    # remove empty lines
    file_content = re.sub(r'\n{3,}', r'\n\n', file_content)

    # footnote to cite
    file_content = re.sub(r'\s*\\footnote{\sKey:(\w*)\s[^}]*\s}', r'~\\cite{\1}', file_content)

    delimiter = '\\chapter{'
    partial_file_header = '% !TEX encoding = utf8\n% !TEX root = ../main.tex\n\n'
    for i, c in enumerate(file_content.split('\\chapter{')):
        if i == 0:
            write_file('abstract.tex', partial_file_header + c, output_path)
        else:
            write_file('chapter_{}.tex'.format(i), partial_file_header + delimiter + c, output_path)

def write_file(file_name, content, output_path):
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, file_name), 'w') as f:
        f.write(content)


if __name__ == '__main__':
    main()