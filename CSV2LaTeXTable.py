#!/usr/bin/env python
# coding: utf-8

# In[3]:


import csv
import logging
import os
import subprocess

class CSV2TEX:
    def __init__(self, csv_filename, latex_filename, bold_header=True, 
                 generate_pdf=True, importan_row_id=0):
        self.csv_filename = csv_filename
        self.latex_filename = latex_filename
        self.bold_header = bold_header
        self.generate_pdf = generate_pdf
        self.importan_row_id = importan_row_id
        
        content = ''
    
    def load_csv():
        pass
    
    def generate_document_header(self):
        doc_header = '\\documentclass[12pt]{article} \n'
        doc_header += '\\usepackage{graphicx} \n'
        doc_header += '\\usepackage[table,xcdraw]{xcolor} \n'
        doc_header += '\\begin{document} \n'
        
        return doc_header
    
    def generate_table_header(self, csv_filename):
        with open(csv_filename, 'r') as csvFile:
            reader = csv.reader(csvFile)
            hd = '|'
            for row in reader:
                for l in range(len(row)):
                        hd += 'l|'
                break
                
        header =  '\\begin{table}[ht] \n'
        header += '\\resizebox{\\textwidth}{!}{ \n'
        header += '\\begin{tabular}{'+hd+'} \n'
        header += '\hline \n'

        return header
    
    def generate_table_content(self, csv_filename):
        with open(csv_filename, 'r') as csvFile:
            table_content = ''
            reader = csv.reader(csvFile)

            ind_impt_row = 0
            for row in reader:
                
                #Destaque para linha importante
                if(ind_impt_row == self.importan_row_id):
                    table_content += '\\rowcolor[HTML]{EFEFEF}'
                    for ind_pct in range(len(row)):
                        row[ind_pct] = '\\textit{' + row[ind_pct] + '}'
                
                # Escape special TeX symbols (%, &, _, #, $)        
                for ind_pct in range(len(row)):
                    if('&' in row[ind_pct]):
                        row[ind_pct] = str(row[ind_pct]).replace('&', '\&')
                    if('%' in row[ind_pct]):
                        row[ind_pct] = str(row[ind_pct]).replace('%', '\%')                        
                        
                #Cabecalho em negrito
                if(self.bold_header):
                    for ind_pct in range(len(row)):
                        row[ind_pct] = '\\textbf{' + row[ind_pct] + '}'
                    self.bold_header = False
                    
                separador = ' &'
                x = ''.join(''.join(p) for p in zip(row,[separador]*len(row)))
                #table_content+=x[:-1].replace('\"','').replace('%', '\%').replace('_','\_')
                table_content+=x[:-1].replace('\"','').replace('_','\_')
                table_content += ' \\\ \hline \n'
                
                ind_impt_row = ind_impt_row + 1
                
        csvFile.close()
        #logging.info(table_content)
        
        return table_content
    
    def generate_table_footer(self):
        footer = '\\end{tabular}\n}\n'
        footer += '\\end{table} \n'

        return footer

    def generate_document_footer(self):
        doc_footer='\end{document} \n'
        return doc_footer
    
    def to_string(self, csv_filename):
        content =  self.generate_document_header()
        content += self.generate_table_header(csv_filename)
        content += self.generate_table_content(csv_filename)
        content += self.generate_table_footer()
        content += self.generate_document_footer()

        return content
    
    def get_output(self, command):
        proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        
        return out
    
    def generate_table_tex_file(self):        
        text_file = open(self.latex_filename, 'w')
        text_file.write(self.to_string(csv_filename))
        text_file.close()

        if(self.generate_pdf):
            command = 'pdflatex '+ self.latex_filename
            print(self.get_output(command))


# In[4]:


latex_filename = 'results.tex'
csv_filename = 'results.csv'
bold_header = True
generate_pdf = True # Garanta que exista o `pdflatex` esteja instalado na máquina
importan_row_id = 1

p1 = CSV2TEX(csv_filename, latex_filename, bold_header=bold_header, 
             generate_pdf=generate_pdf, importan_row_id=importan_row_id)

p1.generate_table_tex_file()


# In[ ]:




