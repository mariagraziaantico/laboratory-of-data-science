# -*- coding: utf-8 -*-

import csv

from aux_functions import create_columns
                   

def iscorrect(filer,filew,name, header, cols=[]):
    #the function simply considers the csv for answers and add the is 
    #correct column as asked by the task
    file_r = open(filer, 'r', newline='')
    reader = csv.reader(file_r)
    file_w = open(filew,'w', newline='')
    writer = csv.writer(file_w)
    header_check = True  
    for row in reader:
        if header_check:
            if header:     
                
                columns = create_columns(cols, row, header).values()

                writer.writerow(row + [name])
                header_check = False
                continue
            else:          
                columns = create_columns(cols, row , header).values()
                header_check = False
                
        
        sub_row = [row[i] for i in range(0,len(row)) if i in list(columns)]
        
        if sub_row[0]==sub_row[1]:
            correct = '1'
        else:
            correct = '0'
        writer.writerow(row + [correct])
    
    file_r.close()
    file_w.close()
    
    
iscorrect("answers_missing_iscorrect.csv", 'answers.csv','iscorrect', header=True, cols = ['correct_answer', 'answer_value'])
                