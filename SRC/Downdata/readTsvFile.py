# import packages
import csv

# read tsv files and write the txt file with ID
ID_file = open('2021-05-23_clean-dataset.txt', 'w')
ID_list = []
with open('2021-05-23_clean-dataset.tsv') as file:
    tsv_file = csv.reader(file, delimiter = "\t")
    for line in tsv_file:
        if len(line[0]) > 10:
            if line[3] == 'en' or line[3] == 'EN':
                ID_file.write(line[0] + '\n')
                ID_list.append(line[0])
    ID_file.close()
    print(len(ID_list))
        
        
