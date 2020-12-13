import requests

main_url = "http://127.0.0.1:5000/"
update_parking_info_url = main_url + "update_parking_details"
insert_parking_info_url = main_url + "insert_parking_details"
get_available_parking_spots_url = main_url + "get_available_parking_spots"
get_booked_parking_spots_url = main_url +"get_booked_parking_spots"
get_all_data_url = main_url + "parking"

# update record
def update_parking_info():
    camera_id = "DAM04"
    parking_slot = "P5"
    license_plate = "MH12 NM 5214"

    data = {"CAMERA_ID": camera_id, "PARKING_SLOT": parking_slot, "LICENSE_PLATE":license_plate}

    print(requests.put(update_parking_info_url, data).text)

# insert record
def insert_parking_info():
    camera_id = "DAM07"
    parking_venue_id = "Westend012"
    parking_slot = "P7"
    license_plate = "MH12 AB 2158"

    data = {"CAMERA_ID": camera_id, "PARKING_VENUE_ID":parking_venue_id,"PARKING_SLOT": parking_slot, "LICENSE_PLATE":license_plate}

    print(requests.post(insert_parking_info_url, data).text)


def get_available_parking_spots():
    print(requests.get(get_available_parking_spots_url).text)

def get_booked_parking_spots():
    print(requests.get(get_booked_parking_spots_url).text)

def get_all_data():
    print(requests.get(get_all_data_url).text)



# update_parking_info()
# insert_parking_info()
# get_available_parking_spots()
# get_booked_parking_spots()
# get_all_data()