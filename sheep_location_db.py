import sys
import sqlite3, csv
import copy
from datetime import datetime as dt
import datetime
sys.path.append('C:\\Python27\\Lib\\site-packages\\MySQLdb')

dbpath = "C:\\Users\\mtags\\Desktop\\sheep.db"

def dosomething():
    results_ei_giver = conn.execute("SELECT * FROM exposure_incident")            
    for row_giver in results_ei_giver.fetchall():
        #print(row_giver['receiver_animal_eid'] + "\t" + row_giver['animal_exposure_date'])

        results_ei_receiver = conn.execute(" \
            select locq.giver_animal_eid, locq.location_cph, locq.location_exposure_date, shpq.animal_eid as receiver_animal_eid, CASE WHEN arrival_date > locq.location_exposure_date then arrival_date else locq.location_exposure_date end AS animal_exposure_date from sheep_location shpq, \
            (select animal_eid as giver_animal_eid, location_cph, min(CASE WHEN arrival_date > ? then arrival_date else ? end) AS location_exposure_date \
            from sheep_location where animal_eid = ? and departure_date >= ? GROUP BY animal_eid, location_cph) as locq \
            where shpq.location_cph = locq.location_cph and shpq.departure_date > locq.location_exposure_date", \
            (row_giver['animal_exposure_date'], row_giver['animal_exposure_date'], row_giver['receiver_animal_eid'], row_giver['animal_exposure_date'], ))
        for row_receiver in results_ei_receiver:
            #print(row_receiver[0] + "\t" + row_receiver[1] + "\t" + row_receiver[2] + "\t" + row_receiver[3] + "\t" + row_receiver[4])
            conn.execute("INSERT INTO exposure_incident (giver_animal_eid, location_cph, location_exposure_date, receiver_animal_eid, animal_exposure_date) VALUES (?, ?, ?, ?, ?)", \
                (row_receiver['giver_animal_eid'], row_receiver['location_cph'], row_receiver['location_exposure_date'], row_receiver['receiver_animal_eid'], row_receiver['animal_exposure_date'],))

    return 


conn = sqlite3.connect(dbpath)
conn.row_factory = sqlite3.Row
#try:

conn.execute("DELETE FROM exposure_incident")
conn.execute("INSERT INTO exposure_incident (receiver_animal_eid, animal_exposure_date) VALUES (?, ?)", ('s1', '2016-02-01',))

dosomething()
dosomething()
dosomething()
#print(infected_sheeps_result)

results_ei_final = conn.execute("SELECT distinct * FROM exposure_incident")            
for row in results_ei_final:
    print(str(row['giver_animal_eid']) + "\t" + str(row['location_cph']) + "\t" + str(row['location_exposure_date']) + "\t" + str(row['receiver_animal_eid']) + "\t" + str(row['animal_exposure_date']))
    
#except:
print("Unexpected error:", sys.exc_info()[0])
#else:
conn.close()