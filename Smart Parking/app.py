from flask import Flask, request, jsonify, render_template
import sqlite3
import pyodbc
import datetime

app = Flask(__name__)

''' Uncomment this code if you want to use SQLite DB'''
# def db_connection():
#     conn = None
#     try:
#         conn = sqlite3.connect('parking_details.sqlite')
    
#     except sqlite3.Error as e:
#         print(e)
#     return conn

def db_connection():
    conn = None
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=ARSONI-T490\SQLEXPRESS;'
                      'Database=SMART_PARKING;'
                      'Trusted_Connection=yes;')
    
    except Exception as e:
        print(e)
    return conn


@app.route('/parking', methods = ['GET', 'POST', 'PUT'])
def parking():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM PARKING_DETAILS")
        parking_details = [
            dict(CAMERA_ID = row[0], PARKING_VENUE_ID = row[1], PARKING_SLOT= row[2], LICENSE_PLATE= row[3],IN_TIME= row[4], OUT_TIME= row[5], IS_AVAILABLE = row[6])
            for row in cursor.fetchall()
        ]
        if parking_details is not None:
            return jsonify(parking_details)
        

@app.route('/get_available_parking_spots', methods=['GET'])
def get_available_parking_spots():
    conn = db_connection()
    cursor = conn.cursor()
 
    if request.method == 'GET':
        cursor = conn.execute("SELECT COUNT(*) AS AVAILABLE_SPOTS FROM PARKING_DETAILS WHERE IS_AVAILABLE='Y'")
        available_spots = [
        dict(count = row[0])
        for row in cursor.fetchall()
    ]
    if available_spots is not None:
        return jsonify(available_spots)

@app.route('/get_booked_parking_spots', methods=['GET'])
def get_booked_parking_spots():
    conn = db_connection()
    cursor = conn.cursor()
 
    if request.method == 'GET':
        cursor = conn.execute("SELECT COUNT(*) AS AVAILABLE_SPOTS FROM PARKING_DETAILS WHERE IS_AVAILABLE='N'")
        available_spots = [
        dict(count = row[0])
        for row in cursor.fetchall()
    ]
    if available_spots is not None:
        return jsonify(available_spots)


@app.route('/update_parking_details', methods=['PUT'])
def update_parking_details():
    conn = db_connection()
 
    if request.method == 'PUT':
        sql = """ UPDATE Smart_parking.dbo.PARKING_DETAILS SET OUT_TIME = GETDATE(),
                 IS_AVAILABLE = 'Y'
                 WHERE CAMERA_ID=? AND
                 PARKING_SLOT=? AND
                 LICENSE_PLATE = ? """
        CAMERA_ID = request.form["CAMERA_ID"]
        PARKING_SLOT = request.form["PARKING_SLOT"]
        LICENSE_PLATE = request.form["LICENSE_PLATE"]
        conn.execute(sql, (CAMERA_ID,PARKING_SLOT,LICENSE_PLATE ))
        conn.commit()
        return "Updated the record", 200


@app.route('/insert_parking_details', methods=['GET', 'POST'])
def insert_parking_details():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        CAMERA_ID = request.form['CAMERA_ID']
        PARKING_VENUE_ID = request.form['PARKING_VENUE_ID']
        PARKING_SLOT = request.form['PARKING_SLOT']
        LICENSE_PLATE = request.form['LICENSE_PLATE']
        sql = """ INSERT INTO PARKING_DETAILS (CAMERA_ID,PARKING_VENUE_ID,PARKING_SLOT, LICENSE_PLATE, IN_TIME, OUT_TIME, IS_AVAILABLE)
                VALUES (?,?,?,?,GETDATE(),Null,'N') """

        cursor = cursor.execute(sql, (CAMERA_ID, PARKING_VENUE_ID, PARKING_SLOT, LICENSE_PLATE))
        conn.commit()
        return f"Parking id created successfully", 201



if __name__ == "__main__":
    app.run()