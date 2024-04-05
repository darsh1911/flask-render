import mysql.connector
import db


def add_vendor(name, email, phone, company, address, city, pincode, employee_count, password):
    connection = db.getdb()
    cursor = connection.cursor(dictionary=True)


    user_query = "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)"
    vendor_query = "INSERT INTO vendors (id, business_name, address, city, pincode, staff_count) VALUES (%s, %s, %s, %s, %s, %s)"

    try:
        cursor.execute(user_query, (name, email, phone, password))
        cursor.fetchall()
        vendor_id = cursor.lastrowid
        print("New user inserted | ID:" + str(vendor_id))

        cursor.execute(vendor_query, (vendor_id, company, address, city, pincode, employee_count))
        cursor.fetchall()

        connection.commit()
        cursor.close()
        connection.close()

        return {'success': True, 'error': ''}

    except mysql.connector.Error as e:
        if e.errno == 1062:
            msg = "An account already exists with this email/phone number."
        else:
            msg = e.msg
        return {'success': False, 'error': msg}

