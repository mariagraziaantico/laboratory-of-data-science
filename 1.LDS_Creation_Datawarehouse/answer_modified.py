# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 11:12:13 2022

@author: maria
"""
import csv


#answermodified changes the name of a sub-set of columns
#from the answer table, to simplify further steps in table 
#uploading phase and further functions


def answermodified(filer,filew,header):
    file_r = open(filer, 'r', newline='')
    reader = csv.DictReader(file_r)
    file_w = open(filew,'w', newline='')
    writer = csv.writer(file_w)
    header_check = True  
    new = {}
    new2 = []
    for row in reader:
        row['SchemeOfWorkId'] = int(float(row['SchemeOfWorkId']))
        row['answer_value'] = row.pop('AnswerValue')
        row['correct_answer'] = row.pop('CorrectAnswer')
        row['country_name'] = row.pop('CountryCode')
        row['region'] = row.pop('Region')
        #new[row['SchemeOfWorkId']] = int(float(row['SchemeOfWorkId']))
        if header:
            writer.writerow(list(row.keys()))
            header = False
        writer.writerow(row.values())
    
    

answermodified('answerdatacorrect.csv','answers_modified.csv',header=True)
            
            
            