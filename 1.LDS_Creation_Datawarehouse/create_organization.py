# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 10:09:17 2022

@author: Alessio
"""


from aux_functions import table_new_id

table_new_id('answers_modified.csv',
                               'organization.csv',
                               header = True,
                               cols=['QuizId','GroupId','SchemeOfWorkId'],
                               id_start= 0,
                               increment=1,
                               id_name = 'organizationid'
                               )


    