from datetime import datetime
from .database import Database

class ContactsModel:
    @staticmethod
    def create(email, name, comment, ip_address):
        db = Database.get_instance()
        conn = db.get_connection()
        try:
            c = conn.cursor()
            c.execute('''
                INSERT INTO contacts (email, name, comment, ip_address)
                VALUES (?, ?, ?, ?)
            ''', (email, name, comment, ip_address))
            conn.commit()
            return {
                'id': c.lastrowid,
                'email': email,
                'name': name,
                'comment': comment,
                'ip_address': ip_address,
                'created_at': datetime.now()
            }
        finally:
            conn.close()

    @staticmethod
    def get_all():
        db = Database.get_instance()
        conn = db.get_connection()
        try:
            c = conn.cursor()
            c.execute('SELECT * FROM contacts ORDER BY created_at DESC')
            contacts = []
            for row in c.fetchall():
                contacts.append({
                    'id': row[0],
                    'email': row[1],
                    'name': row[2],
                    'comment': row[3],
                    'ip_address': row[4],
                    'created_at': datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S')
                })
            return contacts
        finally:
            conn.close()
