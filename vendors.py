import db
import bcrypt


def add_vendor(name, email, phone, company, address, city, pincode, employee_count, password):
    connection = db.getdb()
    cursor = connection.cursor()

    # Encrypt Password For Storage
    salt = bcrypt.gensalt()
    hashedpw = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    user_query = "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)"
    vendor_query = "INSERT INTO vendors (id, business_name, address, city, pincode, staff_count) VALUES (%s, %s, %s, %s, %s, %s)"

    try:
        cursor.execute(user_query, (name, email, phone, hashedpw))
        cursor.fetchall()
        vendor_id = cursor.lastrowid
        print("New user inserted | ID:" + str(vendor_id))

        cursor.execute(vendor_query, (vendor_id, company, address, city, pincode, employee_count))
        cursor.fetchall()

        connection.commit()
        cursor.close()
        connection.close()

        return {'success': True, 'error': ''}

    except connection.Error as e:
        print(e)
        if e.args[0] == 1062:
            msg = "An account already exists with this email/phone number."
        else:
            msg = e.args[1]
        return {'success': False, 'error': msg}


def login(email, password):
    connection = db.getdb()
    cursor = connection.cursor()

    user_query = "SELECT id, name, password, active FROM users WHERE email=%s LIMIT 1"

    try:
        cursor.execute(user_query, (email,))

        if cursor.rowcount > 0:
            result = cursor.fetchone()
            pwd = bytes(result[2], 'utf-8')

            if not(result[3]):
                if bcrypt.checkpw(bytes(password, 'utf-8'), pwd):
                    print("Logged in successfully")
                    return {'success': True, 'id': result[0], 'name': result[1]}
                else:
                    print("Wrong password")
                    return {'success': False, 'error': 'Invalid username/password.'}
            else:
                print("Account inactive")
                return {'success': False, 'error': 'Please activate your account before trying to log in.'}
        else:
            return {'success': False, 'error': 'Invalid username/password'}

    except connection.Error as e:
        print(e)
        msg = e.args[1]
        return {'success': False, 'error': msg}