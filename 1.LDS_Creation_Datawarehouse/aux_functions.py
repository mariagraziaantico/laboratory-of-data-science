# -*- coding: utf-8 -*-

#auxiliary functions

#we define some general functions used in various steps of our
#schema building process

import csv

from datetime import datetime
from math import ceil

#create_columns() has the purpose of finding the right index of
#attributes managed in the functions in which create_columns() is
#exploited, taking into account also the presence or absence of
#header


def create_columns(cols,row,header):
        
    columns = {}
    
    if header:
        for col in cols:
            if col not in row:
                if col not in range(0,len(row)):
                    raise Exception( 'column named ' + str(col) + ' not present')
            for i in range(0,len(row)):
                if row[i] == col:
                    columns[col] = i
                if i == col:
                    columns[col] = i
    else:
        for col in cols:
            if type(col) != type(1):
                raise Exception('Only integer values are accepted as columns when header = False')
            if col not in range(0,len(row)):
                raise Exception( 'column named ' + str(col) + ' not present')
            for i in range(0,len(row)):
                if i == col:
                    columns[col] = i
                
                
    return columns


#string_to_list is used specifically on the input of SubjectId to
#convert the string into a list of strings.

def string_tolist(string):
    obj_list = []
    temp = ''
    for x in string:
        if x == '[' or x == ' ':
            continue
        if x==',' or x == ']':
            obj_list += [temp]
            temp=''
        else:
            temp += x
    return obj_list


def table_new_id(file1, file2, header, cols=[], id_name ='id', id_start = 0, increment = 1, output_type = 'csv' ):
  
    #id_start and increment are parameters used to 
    #handle the integer values that must be defined
    
    
    csvfile_r = open(file1, 'r', newline='')
    reader = csv.reader(csvfile_r)
    
    if cols == []:
        raise Exception('Insert column values to establish id')
    
    columns = []  
    header_check = True        
               
    sub_rows = set() #this will be used to count the presence of possible
                     #duplicates and eventually not consider them for the
                     #writing phase
    
    if output_type == 'dict':
        dict_rows = dict()
        for row in reader:
            if header_check:
                columns = create_columns(cols, row, header).values()
                header_check = False
                if header:
                    continue
                #if an header is present, then the first row is skipped
                
            sub_row = tuple([row[i] for i in sorted(columns)])
            
            if sub_row not in dict_rows:
                dict_rows[sub_row] = id_start
                id_start += increment
        csvfile_r.close()
        
        
        return dict_rows
            
            
    if output_type == 'csv':
        
        with open(file2, 'w', newline='') as csvfile_w:
            writer = csv.writer(csvfile_w)
            for row in reader:
                if header_check:        
                    if header:
                        #if an header is present, we write it in the final csv file...
                        columns = create_columns(cols, row, header).values()
                        writer.writerow([row[i] for i in columns] + [id_name])
                                     
                        header_check=False
                        continue   
                    else:
                        #...otherwise we simply extract the indexes of the columns of
                        #interests and perform a check over the columns
                        columns = create_columns(cols, row, header).values()
                        header_check = False            
                            
                    
                sub_row = tuple([row[i] for i in columns])
                if sub_row not in sub_rows:
                    sub_rows.add(sub_row)
                    writer.writerow(sub_row + (id_start,))
                    id_start += increment
             
           
        
    csvfile_r.close()
    
    

def def_dict(csvfile, unique_tuple = [], id_identifier = ''):
    #the function is used to create a dictionary where every key
    #is a tuple of values coming from a subset of rows of the 
    #csv file and their value is an id linked with that tuple
    
    filer = open(csvfile, 'r', newline='')    
    dict_reader = csv.DictReader(filer)
    new_dict = {}
    for dictionary in dict_reader:
        #introducing a sorting on the unique_tuple parameter,
        #and also in future function, assures us that a user
        #of the function can write the attribute names in any order
        tup = tuple([dictionary[col] for col in sorted(unique_tuple)])
        
        new_dict[tup] = dictionary[id_identifier]
        
    return new_dict, id_identifier

def date_handle(date):
    #the function is used to uniform dates with and without hours/minutes/
    #seconds and distinguish between day, month, year, quarter
    dt = datetime.fromisoformat(date)
    date_format = dt.strftime("%Y-%m-%d")
    day=dt.strftime("%d")
    month=dt.strftime("%m")
    year=dt.strftime("%Y")
    quarter=(ceil(int(month) / 3.0))    
    
    return date_format, day, month, year, quarter


def table_dict(file1,new_csvfile,
                 id_subs={},additional_del_cols=[]):
    #the function is used to build user and answer. id_subs <key,value>
    #must be of the form 
    
    #('organizationid', 'QuizId','GroupId','SchemeOfWorkId' )  : org_dic
    
    #where the first element of the tuple identifies the id that has to
    #substitute in the final csv file all the rest of the columns in
    #the tuple, so for this particular example we say that, as output
    #we want that the new table obtained deletes from each row the values
    #for 'QuizId','GroupId','SchemeOfWorkId' and instead adds the respective
    #value for organizationid, found inside  org_dic, which is a dictionary 
    #of tuples and their respective ids
    
    csvfile1 = open(file1, 'r', newline='')
    csvfile_w = open(new_csvfile, 'w', newline='')
    reader = csv.DictReader(csvfile1)    
    writer = csv.writer(csvfile_w)
    
    written_header = True
    already_written = set()
    for row in reader:
        #we consider each row
        for tup, dictionary in id_subs.items(): 
           
            
            
            values_in_row = ()
            #then for every key, so a tuple, we consider tup[1:],
            #which are the attributes we need to substitue
            
            #we sort the attribute in order to allow the user to
            #specify in the parameters the attributes in any order
            for attribute in sorted(list(tup[1:])):
                #we pop the corresponding value of the attribute and
                #build the tuple we need to confront with the 
                #current dictionary, which is the dictionary related to
                #the actual attribute tuples we are taking into account
                
                #we use a dicstionary to speed up the research process
                #and perform the column substitution reading just
                #one attribute at time
                
                value = row.pop(attribute)  
                #if we are taking into account the dateid, then we 
                #need to perform the transformation to handle DateAnswered
                if tup[0] == 'dateid':
                    value = date_handle(value)[0]
                values_in_row += (value,)
                
            
            id_ref = dictionary[values_in_row] 
            #we find the id correspoding to the tuples <values_in_row>
            #we write the id according to tup[0] being the name of the new
            #column we want to introduce instead of the attributes in tup[1:]
            
            row[tup[0]] = id_ref
            
        for col in additional_del_cols:
            #we add this if condition to eliminate further columns
            #we are not interested with respect to the final result
            del row[col]
            
            
        if written_header:
            writer.writerow(list(row.keys()))
            written_header = False

        #the conversion in tuple is needed, since we can't add
        #a list to a set, and it is preferable to use a set for the 
        #checking if an element has already been read, instead of a list
        row = tuple(row.values())
       
        if row not in already_written:
            already_written.add(row)
            writer.writerow(row)
        
       
    csvfile_w.close()
        
        
