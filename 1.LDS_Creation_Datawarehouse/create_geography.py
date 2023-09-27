# -*- coding: utf-8 -*-



# In order to create the Geography Table, we create the function generate_continent that, given
# a txt file "countryInfo" in which there are informations about different countries and the relative
# continent, create a dictionary in which the key is CountryCode and the value the continent associated.
# Furthermore, in doing this, we considered 'NA' and 'SA', corresponding to North America
# and South America, being part of a unique continent 'AM'. 

# In the end, with the function create_geography which use the output of the generate_continent 
# function, the table Geography is generated in a csv file.

import csv

from aux_functions import create_columns 


def generate_continent(txtfile,columns):
    countryfile = open(txtfile, 'r', newline = '\n')
    dic = {}
    for line in countryfile.readlines():
        tokens = line.strip().split('\t')
        row = []
        #the continent column of txt file(i==8)
        for i in columns:
            if i == 8:
                if tokens[i] == 'NA' or tokens[i] == 'SA':
                    row = row + ['AM']
                else:
                    row = row + [tokens[i]]
        #the countrycode of txt file (i==9)
            if i == 9:
                # not considering the first letter that is, in this columns, a point '.'
                row = row + [tokens[i][1:]]   
                # dictionary with key = countrycode, value = continent
        dic[row[1]] = row[0]
            
    countryfile.close()
    return dic
    

# the dict_compare parameter is, in our case, "country_name"
def create_geography(filer, filew , dic, dict_compare,  header, cols =[],
                    
                     start_id = 0, increment = 1, id_name = 'id'):
    
    file_r = open(filer, 'r', newline = '')
    file_w = open(filew, 'w', newline = '')
    reader = csv.reader(file_r)
    writer = csv.writer(file_w)
    
    for i in cols:
        if type(i) != type(dict_compare):
            raise Exception('Value for dictionary comparisons and columns must be of the same type')
    
    
    header_check = True
    
    final_rows = set()
    
    for row in reader:
        if header_check:
            if header:
                
                columns = create_columns(cols, row, header)
                writer.writerow(['country_name','region'] + ['Continent'] + [id_name])
                header_check = False
                continue
            else:
                columns = create_columns(cols, row, header)
                header_check = False
                
        
    # this represents, using the index of "country_name" column, the country_name value
        region_in_current_row = row[columns[dict_compare]]
        # We find the continent using the dictionary defined in the function above (continents are
        # the key values), using as key the country_name (stored in region_in_current_row) 
        continent = dic[region_in_current_row]
        
        new_row = tuple([row[i] for i in range(0,len(row)) if i in columns.values()] + [continent])
        if new_row not in final_rows:#check for duplicates
            final_rows.add(new_row)
            writer.writerow(new_row + (start_id,))
            start_id += increment
            
    file_r.close()
    file_w.close()
 
continents = generate_continent('countryInfo.txt', [8,9])
        
create_geography('answers_modified.csv', 'geography.csv',
                 continents,  dict_compare='country_name' ,header=True,
                 cols = ['region','country_name'], id_name='geoid')
        

    