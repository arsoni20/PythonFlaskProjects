import sqlite3

conn = sqlite3.connect("parking_details.sqlite")

cursor = conn.cursor()

sql_query = """CREATE TABLE PARKING_DETAILS (CAMERA_ID text,
PARKING_VENUE_ID text,
PARKING_SLOT text,
LICENSE_PLATE text,
IN_TIME text,
OUT_TIME text,
IS_AVAILABLE text)"""

cursor.execute(sql_query)