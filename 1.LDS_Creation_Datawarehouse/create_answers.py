# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 13:27:01 2022

@author: Alessio
"""


from aux_functions import def_dict, table_dict, table_new_id


#the function considers a csv file and outputs a outputs a dictionary
#where every key is a tuple of values of a sub-set of attributes
#of the original column and their respective value is the unique
#identifier associated with that sub-set. The function outputs also
#a name, used in additional functions to identify the dictionary

#the function works properly with csv file having a header, given
#the usage of csv.DictReader
  

date_dic, date_id = def_dict('date.csv', unique_tuple= ['date'], id_identifier='dateid')
org_dic, org_id = def_dict('organization.csv', unique_tuple= ['QuizId','GroupId','SchemeOfWorkId'], id_identifier='organizationid')


subj_dic = table_new_id('answers_modified.csv', '', header=True, cols = ['SubjectId'], output_type='dict')
subj_name =  'subjectid'


cols_to_del = ['Gender','DateOfBirth','PremiumPupil','RegionId','region','country_name']

table_dict('answers_modified.csv','answers_missing_iscorrect.csv',
             id_subs = { ('organizationid', 'QuizId','GroupId','SchemeOfWorkId' )  : org_dic,
                        ('subjectid', 'SubjectId' )  : subj_dic,                         
                         ('dateid', 'DateAnswered' )  : date_dic,
                        },
             additional_del_cols=cols_to_del)

    

    
    
    
    