import csv

ny_city = open('ny_city.csv', 'w', newline='')
la_city = open('la_city.csv', 'w', newline='')
pho_city = open('pho_city.csv', 'w', newline='')
hou_city = open('hou_city.csv', 'w', newline='')
writer1 = csv.writer(ny_city, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer2 = csv.writer(la_city, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer3 = csv.writer(pho_city, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer4 = csv.writer(hou_city, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

lines_list = []
county_list_1 = ['Bronx County', 'Kings County', 'New York County', 'Queens County', 'Richmond County']
county_list_2 = ['Los Angeles County', 'Orange County', 'Riverside County', 'San Bernardino County', 'Ventura County']
county_list_3 = ['Apache County', 'Cochise County', 'Coconino County', 'Gila County', 'Graham County', 'Greenlee County', 'La Paz County',
                 'Maricopa County', 'Mohave County', 'Navajo County', 'Pima County', 'Pinal County', 'Santa Cruz County', 'Yavapai County', 'Yuma County']
county_list_4 = ['Austin County', 'Brazoria County', 'Chambers County', 'Fort Bend County', 'Galveston County', 'Harris County', 
                 'Liberty County', 'Montgomery County', 'Waller County']

with open('Vaccinations County.csv') as myfile:
    title = myfile.readline()
    title_list = title.split(',')
    writer1.writerow(title_list)
    writer2.writerow(title_list)
    writer3.writerow(title_list)
    writer4.writerow(title_list)
    lines = myfile.readlines()
    for i in range(len(lines)):
        line = lines[i].split(',')
        lines_list.append(line)
    for j in range(len(lines_list)):
        if lines_list[j][4] == 'NY':
            for item in county_list_1:
                if item == lines_list[j][3]:
                      writer1.writerow(lines_list[j])
        if lines_list[j][4] == 'CA':
            for item in county_list_2:
                if item == lines_list[j][3]:
                     writer2.writerow(lines_list[j])
        if lines_list[j][4] == 'TX':
            for item in county_list_4:
                if item == lines_list[j][3]:
                     writer4.writerow(lines_list[j])
        if lines_list[j][4] == 'AZ':
            for item in county_list_3:
                if item == lines_list[j][3]:
                     writer3.writerow(lines_list[j])
ny_city.close()
la_city.close()
hou_city.close()
pho_city.close()