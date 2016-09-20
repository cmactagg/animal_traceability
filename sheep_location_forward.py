import sys
import sqlite3, csv
import copy
from datetime import datetime as dt
import datetime
sys.path.append('C:\\Python27\\Lib\\site-packages\\MySQLdb')

dbpath = "C:\\Users\\mtags\\Desktop\\sheep.db"

def dosomething(conn, infected_sheeps_input):
    new_rec_found = False
    infected_sheeps_output = copy.deepcopy(infected_sheeps_input)
    #infected_sheeps_output.deepcopy(infected_sheeps_input)
    for sp in infected_sheeps_input:
        #print(loc + " " + infected_loc_dict[loc])
        resultsR2 = conn.execute(\
            "select animal_eid, min(CASE WHEN arrival_date > locq.exposure_date then arrival_date else locq.exposure_date end) AS exposure_date from sheep_location shpq, \
            (select location_cph, min(CASE WHEN arrival_date > ? then arrival_date else ? end) AS exposure_date \
            from sheep_location where animal_eid = ? and departure_date >= ? GROUP BY location_cph) as locq \
            where shpq.location_cph = locq.location_cph and shpq.departure_date > locq.exposure_date GROUP BY animal_eid", \
            (infected_sheeps_input[sp], infected_sheeps_input[sp], sp, infected_sheeps_input[sp],))
        for rowR2 in resultsR2:
            #print('ddd' + str(rowR2))
            if rowR2[0] not in infected_sheeps_output or infected_sheeps_output[rowR2[0]] > rowR2[1]:
                infected_sheeps_output[rowR2[0]] = rowR2[1]                
                new_rec_found = True
    if new_rec_found:
        print(infected_sheeps_output)
        infected_sheeps_output = dosomething(conn, infected_sheeps_output)

    return infected_sheeps_output


connX = sqlite3.connect(dbpath)

#try:
infected_sheeps = {'s1': '2016-01-01'}

infected_sheeps_result = dosomething(connX, infected_sheeps)
print(infected_sheeps_result)
#except:
print("Unexpected error:", sys.exc_info()[0])
#else:
connX.close()