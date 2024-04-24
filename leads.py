import db


def new_lead(email):
    print(email)
    connection = db.getdb()
    cursor = connection.cursor()

    query = "INSERT INTO leads (email, type) VALUES (%s, 'user')"
    try:
        cursor.execute(query, email)
        lead_id = cursor.lastrowid
        print("New lead inserted | ID:" + str(lead_id))

        connection.commit()
        cursor.close()
        connection.close()

        return {'success': True, 'error': ''}

    except connection.Error as e:
        print(e)
        if e.args[0] == 1062:
            msg = "An request already exists with this email/phone number."
        else:
            msg = e.args[1]
        return {'success': False, 'error': msg}
