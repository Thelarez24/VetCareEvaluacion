import sqlite3
from datetime import datetime
from pathlib import Path

class Database:
    _instance = None
    
    @classmethod
    def initialize(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError('Database not initialized. Call Database.initialize() first.')
        return cls._instance

    def __init__(self):
        if Database._instance is not None:
            raise RuntimeError('Use Database.initialize() to create an instance.')
        
        self.db_path = Path(__file__).parent.parent / 'database' / 'vetcare.db'
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(str(self.db_path))

    def init_db(self):
        conn = self.get_connection()
        try:
            c = conn.cursor()
            
            # Create contacts table
            c.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    name TEXT NOT NULL,
                    comment TEXT NOT NULL,
                    ip_address TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create payments table
            c.execute('''
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    cardholder_name TEXT NOT NULL,
                    amount REAL NOT NULL,
                    currency TEXT NOT NULL,
                    service TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
        finally:
            conn.close()
