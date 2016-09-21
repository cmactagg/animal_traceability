import sys
import sqlite3, csv
import copy
from datetime import datetime as dt
import datetime
sys.path.append('C:\\Python27\\Lib\\site-packages\\MySQLdb')

dbpath = "C:\\Users\\mtags\\Desktop\\sheep.db"

def dosomething():
    isNewRecordsCreated = False
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
            
            doInsertRecord = True
            cursor = conn.cursor()
            #check that the giver and receiver animal arent the same
            if row_receiver['giver_animal_eid'] == row_receiver['receiver_animal_eid']:
                doInsertRecord = False

            #check that you arent exposing an animal that exposed you
            cursor.execute( \
                "SELECT giver_animal_eid FROM exposure_incident \
                WHERE giver_animal_eid = ? AND receiver_animal_eid = ? LIMIT 1", \
                (row_receiver['receiver_animal_eid'], row_receiver['giver_animal_eid'],))
            if cursor.fetchone() is not None:
                doInsertRecord = False

            #check to ensure record doesnt exist already
            
            cursor.execute( \
                "SELECT giver_animal_eid FROM exposure_incident \
                WHERE giver_animal_eid = ? AND location_cph = ? AND location_exposure_date = ? AND receiver_animal_eid = ? AND animal_exposure_date = ? LIMIT 1", \
                (row_receiver['giver_animal_eid'], row_receiver['location_cph'], row_receiver['location_exposure_date'], row_receiver['receiver_animal_eid'], row_receiver['animal_exposure_date'],))
            if cursor.fetchone() is not None:
                doInsertRecord = False

            if doInsertRecord:
                conn.execute("INSERT INTO exposure_incident (giver_animal_eid, location_cph, location_exposure_date, receiver_animal_eid, animal_exposure_date) VALUES (?, ?, ?, ?, ?)", \
                    (row_receiver['giver_animal_eid'], row_receiver['location_cph'], row_receiver['location_exposure_date'], row_receiver['receiver_animal_eid'], row_receiver['animal_exposure_date'],))
                isNewRecordsCreated = True
            cursor.close()
            if isNewRecordsCreated:
                dosomething()
    return 


conn = sqlite3.connect(dbpath)
conn.row_factory = sqlite3.Row
#try:

conn.execute("DELETE FROM exposure_incident")
conn.execute("INSERT INTO exposure_incident (receiver_animal_eid, animal_exposure_date) VALUES (?, ?)", ('s1', '2016-02-01 00:00:00.000',))

dosomething()

#print(infected_sheeps_result)

results_ei_final = conn.execute("SELECT * FROM exposure_incident")            
for row in results_ei_final:
    print(str(row['giver_animal_eid']) + "\t" + str(row['location_cph']) + "\t" + str(row['location_exposure_date']) + "\t" + str(row['receiver_animal_eid']) + "\t" + str(row['animal_exposure_date']))
    
#except:
print("Unexpected error:", sys.exc_info()[0])
#else:
conn.close()


# todo:
# cant expose to a previous location (split the day in half, or thirds (departure, waystation, destination))
    # you cant expose to another sheep on the day you were initially exposed
        #but what if you were in 3 locations in one day (carrying the exposure from loc2 to loc3, but not back to loc1)

