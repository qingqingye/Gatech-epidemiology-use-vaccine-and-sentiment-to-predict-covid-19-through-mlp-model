from datetime import datetime

def allCounty(writefile, openfile, end):
    countydata = open(writefile, 'w')
    countydata.write('date,cases,deaths' + '\n')
    
    time_list = {}
    lines_list = []
    with open(openfile) as myfile:
        lines = myfile.readlines()
        for i in range(len(lines)):
            line = lines[i].split(',')
            lines_list.append(line) 
        
        for j in range(len(lines_list)):  
            time = datetime.strptime(lines_list[j][0], '%Y-%m-%d')
            if time <= end:
                if time not in time_list:
                    time_list[time] = (int(lines_list[j][4]), int(lines_list[j][5]))
                else:
                    temp = time_list[time]
                    update = (int(lines_list[j][4]) + temp[0], int(lines_list[j][5]) + temp[1])
                    time_list[time] = update
        
    for key in time_list:
        temp_1 = str(time_list[key][0])
        temp_2 = str(time_list[key][1])
        key_time = str(key)
        countydata.write(key_time + ',' + temp_1 + ',' + temp_2 + '\n')
    countydata.close()
    
endtime = datetime.strptime('2021-10-31', '%Y-%m-%d')
allCounty('hou_allcounty.txt', 'hou_city.txt', endtime)
allCounty('la_allcounty.txt', 'la_city.txt', endtime)
allCounty('ny_allcounty.txt', 'ny_city.txt', endtime)
allCounty('pho_allcounty.txt', 'pho_city.txt', endtime)
        
