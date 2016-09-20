import sys
import sqlite3, csv
from datetime import datetime as dt
import datetime
sys.path.append('C:\\Python27\\Lib\\site-packages\\MySQLdb')

dbpath = "C:\\Users\\mtags\\Desktop\\sheep.db"

def dosomething(conn, infected_sheeps):
    print("entering dosomething")
    new_rec_found = False
    infected_loc_dict = {}
    # 1. identify the infected sheep
    for infected_sheep in infected_sheeps:
        # 2. store all the locations that the infected sheep(s) was at and the date range that the location was infected
        
        results = conn.execute( \
            "SELECT location_cph, min(arrival_date) FROM sheep_location WHERE animal_eid = ? AND departure_date >= ? GROUP BY location_cph", \
                (infected_sheep, infected_sheeps[infected_sheep]))
        for row in results:
            infected_loc_dict[row[0]] = row[1];
            

    print(infected_loc_dict)    
    #infected_sheeps = {};
# 3. search all sheep for the infected location/time range
    for loc in infected_loc_dict:
        #print(loc + " " + infected_loc_dict[loc])
        resultsR2 = conn.execute(\
            "SELECT animal_eid, min(arrival_date) FROM sheep_location WHERE location_cph = ? AND departure_date > ? GROUP BY animal_eid", \
                (loc, infected_loc_dict[loc],))
        
        #print('aaa' + str(infected_sheeps))
        for rowR2 in resultsR2:
            print('ddd' + str(rowR2))
            if rowR2[0] not in infected_sheeps or infected_sheeps[rowR2[0]] > rowR2[1]:
                #print(str(rowR2[0] not in infected_sheeps))                
                #if rowR2[0] in infected_sheeps:
                    #print('\t' + str(infected_sheeps[rowR2[0]] > rowR2[1]))
                
                infected_sheeps[rowR2[0]] = rowR2[1]                
                new_rec_found = True
    if new_rec_found:
        print(infected_sheeps)
        infected_sheeps = dosomething(conn, infected_sheeps)
            
    return infected_sheeps



connX = sqlite3.connect(dbpath)

#try:
#d = datetime.date(2016, 1, 1)
s = '2016-04-01'

infected_sheeps = {'s1': s}

infected_sheeps_result = dosomething(connX, infected_sheeps)
print(infected_sheeps_result)
#except:
print("Unexpected error:", sys.exc_info()[0])
#else:
connX.close()