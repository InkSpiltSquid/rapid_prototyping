import sqlite3
from datetime import datetime

class SensorDatabase:
    def __init__(self, db_name="hum_temp_data.db"):
        """Initialize database connection and create table if needed"""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()
    
    def _create_table(self):
        """Create the sensor readings table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                temperature REAL,
                humidity REAL
            )
        ''')
        self.conn.commit()
    
    def add_reading(self, temperature, humidity):
        """Add a new sensor reading with current timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO sensor_readings (timestamp, temperature, humidity)
            VALUES (?, ?, ?)
        ''', (timestamp, temperature, humidity))
        self.conn.commit()
        print(f"Saved: {timestamp} - Temp: {temperature}, Humidity: {humidity}")
    
    def get_all_readings(self):
        """Retrieve all sensor readings"""
        self.cursor.execute('SELECT * FROM sensor_readings ORDER BY id DESC')
        return self.cursor.fetchall()
    
    def get_recent_readings(self, limit=10):
        """Get the most recent N readings"""
        self.cursor.execute(
            'SELECT * FROM sensor_readings ORDER BY id DESC LIMIT ?', 
            (limit,)
        )
        return self.cursor.fetchall()
    
    def close(self):
        """Close database connection"""
        self.conn.close()