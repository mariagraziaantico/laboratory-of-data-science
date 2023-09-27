# -*- coding: utf-8 -*-



import pyodbc
import csv

## connecting to the server
server = 'tcp:lds.di.unipi.it' 
database = 'Group_7_DB' 
username = 'Group_7' 
password = 'SS1JOL7N' 
connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()


def define_dictionarty(file_name):
    #the function outputs a DictReader object that is an iterable 
    #which, when looped over, outputs a dictionary for the rows of the
    #csv file
    handler = open(file_name, 'r', newline = '')
    dict_object = csv.DictReader(handler)

    return dict_object, dict_object.fieldnames



#the general_db functions considers a csv file and a table's name in
#an external server's database, and given a cursor, 
#performs an insertion of the values of the csv records on the 
#table in the server



def general_db(filer, table_name, cursor, delete_all = True, failure_row = 1): 
    #square brackets are introduced to avoid ambiguities with keywords, i.e. user table
    
    
    table = '[' + table_name + ']'
    #we add an additional condition to check the existence of the 
    
    #table before any racord insertion
    obj_exists = "IF OBJECT_ID(N'{}', N'U') IS NOT NULL".format(table)
    
    #delete all is an optional parameter that deletes the content of the whole
    #table before starting the new values insertions
    if delete_all:
        delete = "DELETE FROM {}".format(table)
        cursor.execute(obj_exists + ' ' +  delete)
        cursor.commit()
    
        
    data = define_dictionarty(filer) #data stores the dict_reader object
    header = data.fieldnames #header stores the header of the csv
    insert = 'INSERT INTO'
   
    
    #columns is used to obtain a string corresponding to
    #the columns of the table we want to write according to
    columns = '('
    for col in header:
        columns += '[' + col +']' +', '
    columns = columns[:-2] +')'
    columns = columns.lower()
    
    initialize_missing, initialize = (), True

    for row in data:
        #for the first row, we initialize a string of the form (?,?,...,?)
        #with the same number of question marks equivalent to the records' lenght
        #in order to perform the writing of the query        
        if initialize:
            for el in range(0,len((row.keys()))):
                initialize_missing += (1,) 
                initialize = False
                
        initialize_missing = str(initialize_missing).replace('1','?')
        
        #sql defines the final string for the queries
        sql = insert + ' ' + table + ' ' + columns + ' ' + 'VALUES' + ' ' + initialize_missing

        values_to_write = tuple(row.values())
    
        #we execute the query with the cursor
        cursor.execute(obj_exists + ' ' + sql, values_to_write)
        cursor.commit()
        
                
        
#we first fill the tables having no foreing keys towards other tables
#in the datawarehouse

#before eliminating the values in Date, Organization, Subject and
#Geography, the records from User and Answer must be eliminated
#in order to avoid conflicts of foreing keys.

#the next part of the code, where we execute for each table the
#general_db function, is commented in order to avoid executing
#long queries, after having already performed the table uploading 
#filling the schema on the remote server. 

'''
cursor.execute('DELETE FROM [User]')
cursor.commit()

cursor.execute('DELETE FROM [Answer]')
cursor.commit()

general_db('date.csv','Date', cursor)

general_db('subject.csv','Subject', cursor)

general_db('geography.csv','Geography', cursor)

general_db('organization.csv','Organization',  cursor)

#we then proceed with tables having foreign keys

general_db('user.csv','User', cursor)

general_db('answers.csv','Answer', cursor, delete_all=True)


'''

cursor.close()
cnxn.close()


