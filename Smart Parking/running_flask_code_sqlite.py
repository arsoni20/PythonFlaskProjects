from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# parking_list = [{
#     "id":1,
#     "cam":"CAM01"
# }]


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('parking_details.sqlite')
    
    except sqlite3.Error as e:
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

    if request.method == 'POST':
        CAMERA_ID = request.form['CAMERA_ID']
        PARKING_VENUE_ID = request.form['PARKING_VENUE_ID']
        PARKING_SLOT = request.form['PARKING_SLOT']
        LICENSE_PLATE = request.form['LICENSE_PLATE']
        IN_TIME = request.form['IN_TIME']
        OUT_TIME = request.form['OUT_TIME']
        IS_AVAILABLE = request.form['IS_AVAILABLE']
        sql = """ INSERT INTO PARKING_DETAILS (CAMERA_ID,PARKING_VENUE_ID,PARKING_SLOT, LICENSE_PLATE,IN_TIME,OUT_TIME,IS_AVAILABLE )
                VALUES (?,?,?,?,?,?,?) """
        cursor = cursor.execute(sql, (CAMERA_ID,PARKING_VENUE_ID,PARKING_SLOT, LICENSE_PLATE,IN_TIME,OUT_TIME,IS_AVAILABLE))
        conn.commit()
        return f"Parking with id:{cursor.lastrowid} created successfully", 201
        

@app.route('/get_parking_details', methods=['GET'])
def get_parking_details():
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



# @app.route('/get_parking_details/<int:id>', methods=['GET', 'PUT'])

# def get_parking_available(id):
#     if request.method == 'GET':
#         for i in parking_list:
#             if i["id"] == id:
#                 return jsonify(i)
#             pass

if __name__ == "__main__":
    app.run()