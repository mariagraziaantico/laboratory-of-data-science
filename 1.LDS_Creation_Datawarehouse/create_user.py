# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 13:27:01 2022

@author: Alessio
"""

import csv
from aux_functions import def_dict, table_dict, date_handle


#the function considers a csv file and outputs a outputs a dictionary
#where every key is a tuple of values of a sub-set of attributes
#of the original column and their respective value is the unique
#identifier associated with that sub-set. The function outputs also
#a name, used in additional functions to identify the dictionary

#the function works properly with csv file having a header, given
#the usage of csv.DictReader
  

date_dic, date_id = def_dict('date.csv', unique_tuple= ['date'], id_identifier='dateid')
geo_dic, geo_id = def_dict('geography.csv', unique_tuple= ['region','country_name'], id_identifier='geoid')

#we take into account the dictionaries of tuple of geo and date
        
cols_to_del = ['QuestionId','AnswerId','correct_answer','answer_value',
               'PremiumPupil','DateAnswered','Confidence','GroupId','QuizId',
               'SchemeOfWorkId','SubjectId','RegionId']

#we use table_dict to build the final user table

table_dict('answers_modified.csv','user.csv',
             id_subs = { ('geoid', 'country_name','region' )  : geo_dic,
                        ('dateofbirthid', 'DateOfBirth' )  : date_dic,
                        },
             additional_del_cols=cols_to_del)




    

    
    
    
    