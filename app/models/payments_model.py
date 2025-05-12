from datetime import datetime
from .database import Database

class PaymentsModel:
    @staticmethod
    def create(email, cardholder_name, amount, currency, service):
        db = Database.get_instance()
        conn = db.get_connection()
        try:
            # Validación adicional
            if not isinstance(amount, (int, float)):
                raise ValueError('El monto debe ser un número')
            if amount <= 0:
                raise ValueError('El monto debe ser mayor a 0')
            if not currency in ['USD', 'EUR', 'GBP']:
                raise ValueError('Moneda no válida')

            c = conn.cursor()
            
            # Verificar si ya existe un pago con los mismos datos en los últimos 5 minutos
            c.execute('''
                SELECT COUNT(*) FROM payments
                WHERE email = ? AND amount = ? AND service = ?
                AND created_at > datetime('now', '-5 minutes')
            ''', (email, amount, service))
            
            if c.fetchone()[0] > 0:
                raise ValueError('Pago duplicado detectado. Por favor, espere unos minutos antes de intentar nuevamente.')

            # Insertar el nuevo pago
            c.execute('''
                INSERT INTO payments (email, cardholder_name, amount, currency, service)
                VALUES (?, ?, ?, ?, ?)
            ''', (email, cardholder_name, amount, currency, service))
            
            conn.commit()
            
            # Obtener el pago recién creado
            c.execute('SELECT * FROM payments WHERE id = ?', (c.lastrowid,))
            row = c.fetchone()
            
            return {
                'id': row[0],
                'email': row[1],
                'cardholder_name': row[2],
                'amount': row[3],
                'currency': row[4],
                'service': row[5],
                'created_at': datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            conn.rollback()
            print(f"Error creating payment: {e}")
            raise
        finally:
            conn.close()

    @staticmethod
    def get_all():
        db = Database.get_instance()
        conn = db.get_connection()
        try:
            c = conn.cursor()
            c.execute('SELECT * FROM payments ORDER BY created_at DESC')
            payments = []
            for row in c.fetchall():
                payments.append({
                    'id': row[0],
                    'email': row[1],
                    'cardholder_name': row[2],
                    'amount': row[3],
                    'currency': row[4],
                    'service': row[5],
                    'created_at': datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S')
                })
            return payments
        finally:
            conn.close()
