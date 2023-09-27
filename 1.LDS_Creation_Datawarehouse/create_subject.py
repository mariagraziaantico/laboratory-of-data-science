# -*- coding: utf-8 -*-


import csv

from aux_functions import create_columns, string_tolist



## con ordered_subject viene generata in output una lista di tuple contenenti rispettavemente
## un id (per ogni subject id differente), la lista subjectid ordinata e la descrizione ordinata
## Ouput example: [(0, ['3', '101', '342', '115'], 'Maths - Data and Statistics - Data Representation - Scatter Diagram')...



# Furthermore, the function subject_id_table takes the output of the ordered_subject function
# and, if output_style=='dict', generates a dictionary in which keys are list ordered of subjectid
# and values are associated ids. If the output_style=='csv', the function generates the Subject
# Table in a csv file.



def ordered_subject(ids,metadata, col, header, start_id=0,increment = 1):
    s_ids = open(ids, 'r', newline='')
    reader_s_ids = csv.reader(s_ids)
    met = open(metadata,'r', newline='')
    meta = csv.reader(met)
    # read subject metadata
    list_meta = [x for x in meta][1:] 
    #skipping header [1:]
    list_meta_level = {val[0] : (val[1], int(val[3])) for val in list_meta}
# ... { '34': ('Upper and Lower Bounds', 3), ...} output example of lista_meta_level
    
   
       
    final_out = []
    check = set()
    header_check = True
    for row in reader_s_ids:
        if header_check:
            col = list(create_columns([col], row, header).values())[0]
            header_check = False
            continue
        else:
            col = list(create_columns([col], row, header).values())[0]
            header_check = False
           
        # convert subjectid from string to list
        ids = string_tolist(row[col])
        level, description = [], []
        for x in ids:
            # lista_meta_level[x][1] refers to level of a single subject x
            level.append(list_meta_level[x][1])
            # list_meta_level[x][0] refers to descriptio of a single subject x
            description.append(list_meta_level[x][0])

        tup = list(zip(ids, level, description))
        # sort by level 
        sort = list(sorted(tup, key=lambda x: x[1])) #ordino in base al livello
        subject_ids, subject_description = [], []

        for e in sort:
            # append the subjectid in order
            subject_ids.append(e[0])
            # append the description in order
            subject_description.append(e[2])

    # check for duplicates
        if str(subject_description) in check:
            continue
        else:
            check.add(str(subject_description))
            final_out.append(tuple([start_id] + [subject_ids] + [' - '.join(subject_description)]))
            start_id += increment
            
            
    return final_out




### prendendo in input la lista della funzione precente, genero csv o dict

def subject_id_table(ids,metadata,new_csvfile, header, col, output_style = 'csv'):  
    
    output = ordered_subject(ids,metadata, col, header)
    
    #output example
    #''.. [0,['3', '101', '342', '115'],'"Maths - Data and Statistics - Data Representation - Scatter Diagram"']..''
    if output_style =='csv':
        
        csvfile_w = open(new_csvfile, 'w', newline='')
        writer_header = csv.writer(csvfile_w, delimiter = ',')

        writer = csv.writer(csvfile_w, delimiter = ',', quoting=csv.QUOTE_NONNUMERIC)
      
            
        if header:
            writer_header.writerow(['subjectid'] + ['description'])
            
            
        for x in output:
            writer.writerow((x[0],x[2]))  #x[0]=subjectid, x[2] = descriotionù
           
        csvfile_w.close()
    
    if output_style == 'dict':
        dic = {}
        for x in output:
            
            dic = {}
            for x in output:
                dic[str(x[1])]=x[0]  #x[1] = lista ordinata di subject id
                
            return dic
            
        return dic

subject_id_table('answers_modified.csv','subject_metadata.csv','subject.csv', header=True, col='SubjectId', output_style='csv')
