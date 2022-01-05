ny_city = open('ny_city.txt', 'w')
la_city = open('la_city.txt', 'w')
pho_city = open('pho_city.txt', 'w')
hou_city = open('hou_city.txt', 'w')
county_list_1 = ['Bronx', 'Kings', 'New York', 'Queens', 'Richmond']
county_list_2 = ['Los Angeles', 'Orange', 'Riverside', 'San Bernardino', 'Ventura']
county_list_3 = ['Apache', 'Cochise', 'Coconino', 'Gila', 'Graham', 'Greenlee', 'La Paz',
                 'Maricopa', 'Mohave', 'Navajo', 'Pima', 'Pinal', 'Santa Cruz', 'Yavapai', 'Yuma']
county_list_4 = ['Austin', 'Brazoria', 'Chambers', 'Fort Bend', 'Galveston', 'Harris', 
                 'Liberty', 'Montgomery', 'Waller']
lines_list = []
with open('us-counties.txt') as myfile:
    title = myfile.readline()
    lines = myfile.readlines()
    for i in range(len(lines)):
        line = lines[i].split(',')
        lines_list.append(line)
    for j in range(len(lines_list)):
        if lines_list[j][2] == 'New York':
            if lines_list[j][1] == 'New York City':
                ny_city.write(lines[j])          
        if lines_list[j][2] == 'California':
            for item in county_list_2:
                if item == lines_list[j][1]:
                    la_city.write(lines[j])
        if lines_list[j][2] == 'Arizona':
            for item in county_list_3:
                if item == lines_list[j][1]:
                    pho_city.write(lines[j])
        if lines_list[j][2] == 'Texas':
            for item in county_list_4:
                if item == lines_list[j][1]:
                    hou_city.write(lines[j])
                    
ny_city.close()
la_city.close()
pho_city.close()
hou_city.close()
                