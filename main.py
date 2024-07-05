import requests
from flask import Flask, request
import mysql.connector
import time

app = Flask(__name__)

@app.route("/ayib&ofe8782bf#V.Gjkv33##]/#79bdk/;sa", methods=['POST'])
def hello_world():
    a = request.get_json()
    RFID_ID, timestamp, SCANNER_ID, ACTIVITY = (a['RFID_ID'], a['timestamp'], a['SCANNER_ID'], a['ACTIVITY'])
    cnx = mysql.connector.connect(user='MNami', password='sanusi73',
                                  host='MNami.mysql.pythonanywhere-services.com',
                                  database='MNami$Pelajar')
    dbcursor = cnx.cursor()
    dbcursor.execute(f"SELECT * FROM MNami$Pelajar WHERE RFID_ID = \'{RFID_ID}\'")
    myresult = dbcursor.fetchall()
    time_api_request = requests.get("http://worldtimeapi.org/api/Asia/Kuching").json()
    raw_datetime = time_api_request["datetime"].split("T")
    tarikh, masa = raw_datetime[0], raw_datetime[1].split(":")
    h, m, s = masa[0], masa[1], masa[2]
    if len(myresult) == 0:
        print(f"{time.clock()} - No data found - {RFID_ID}")
        #TODO: make this send data to google sheet
        return {"Message": "Invalid Card", "status": "401"}
    elif len(myresult) == 1:
        student_id, ic, rfid_id, name, email, phonenumber, dorm, kelas, asrama = myresult
        dbcursor.execute(f"SELECT * FROM MNami$Kehadiran WHERE IC = \'{ic}\'")
        resultdbkehadiran = dbcursor.fetchall()
        ic, status, lasttimelogin = resultdbkehadiran
        if lasttimelogin == tarikh:
            return {"Message": "Already Signed", "status": 400}
        if int(h) <= 7:
            if int(m) <= 20:
                status_kehadiran = "hadir_awal"
            else:
                status_kehadiran = "hadir_lewat"
        else:
            status_kehadiran = "tidak_hadir"
        dbcursor.execute(f"UPDATE MNami$Kehadiran SET status=\'{status_kehadiran}\' SET lasttimesigned=\'{tarikh}\' WHERE IC = \'{ic}\'")
        #TODO: append google sheet
        return {"Name": name, "status": 200}
    else:
        print(f"{time.clock()} - Multiple/Duplicate data found - {RFID_ID}")
        #TODO: make this send data to google sheet
        return {"Message": "Multiple/Duplicate Data Found", "status": 400}

if __name__ == '__main__':
    app.run()