# -*- coding: utf-8 -*-


import csv


from aux_functions import create_columns, date_handle


# The function create_date_table , using also the date_handle function, has two possible output_style,
# 'csv' and 'dict'. If output_style == 'dict', the function returns a dictionary in which the keys are
# the date in format YYYY-MM-DD and the value the id associate. If output_style == 'csv', the functions
# write in a file csv the table Date with the relative attributes and values.




def create_date_table(filer,filew,header, date_cols = [], 
                       output_style = 'csv', id_name = 'id',id_start = 0, increment = 1):
    
    csvfile_r = open(filer, 'r', newline='')
    reader = csv.reader(csvfile_r)
    header_check = True
    
    if output_style == 'dict':
        dict_rows = dict()
        for row in reader:
            
            if header_check:
                
                columns = create_columns(date_cols, row, header).values()
                header_check = False
                if header:
                    continue
            new_row = [row[i] for i in range(0,len(row)) if i in columns]
            for date in new_row:
                # date_handle(date)[0] refers to the first output of the date_handle
               # function, which is the date trasformed in YYYY-MM-DD
                dt = (date_handle(date)[0],)
                if dt not in dict_rows:
                    # key = date transformed, value = id associated
                    dict_rows[dt] = id_start
                    id_start += increment
           
        csvfile_r.close()            
        return dict_rows
    
    if output_style == 'csv':
        
        with open(filew, 'w', newline='') as csvfile_w:
            writer = csv.writer(csvfile_w)
            final_rows = set()
            for row in reader:
                if header_check:        
                    if header:
                        #header of the new file
                        new_header = ['date', 'day', 'month', 'year', 'quarter', id_name]
                        #index of the columns in date_cols
                        columns = create_columns(date_cols, row, header).values()
                        writer.writerow(new_header)                                     
                        header_check=False
                        continue
                    else:
                        columns = create_columns(date_cols, row, header).values()
                        header_check = False
                 # in this case, new_row contain the values of DateofBirth and DateAnswered    
                new_row = [row[i] for i in range(0,len(row)) if i in columns]
                for date in new_row:
                    # transform the dates
                    date_format, day, month, year, quarter = date_handle(date)
                    # check if date is already present
                    if date_format not in final_rows:
                        final_rows.add(date_format)
                        writer.writerow([date_format, day, month, year, quarter] + [id_start])
                        id_start += increment
                        
        csvfile_r.close()
                        
        
create_date_table('answers_modified.csv','date.csv',header=True, 
                      date_cols = ['DateOfBirth','DateAnswered'], 
                      output_style = 'csv', id_name = 'dateid')
