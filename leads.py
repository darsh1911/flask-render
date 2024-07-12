import db
import validations as vl


def new_lead(name='', phone='', type='vendor'):
    """
    :param name: string
    :type phone: string
    """
    connection = db.getdb()
    cursor = connection.cursor()
    valid_phone = vl.validate_phone(phone)
    if not valid_phone['success']:
        return valid_phone
    query = "INSERT INTO leads (name, phone, type) VALUES (%s, %s, %s)"
    try:
        data = (name, phone, type)
        cursor.execute(query, data)
        lead_id = cursor.lastrowid
        print("New lead inserted | ID:" + str(lead_id))

        connection.commit()
        cursor.close()
        connection.close()

        return {'success': True, 'error': ''}

    except connection.Error as e:
        print(e)
        if e.args[0] == 1062:
            msg = "The record already exists."
        else:
            msg = e.args[1]
        return {'success': False, 'error': msg}
