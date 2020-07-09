import sqlite3

class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('sensor.db')
        self.create_temperature_table()

    def create_temperature_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "temperature" (
          id INTEGER PRIMARY KEY,
          value REAL NOT NULL,
          timestamp TEXT NOT NULL
        );
        """

        self.conn.execute(query)

class TemperatureModel:
    def __init__(self):
        self.conn = sqlite3.connect('sensor.db')

    def get(self):
        query = 'SELECT * FROM temperature;'
        result = self.conn.execute(query)
        return list(map(lambda x: {
                'temperature': x[1],
                'timestamp': x[2]
            }, result.fetchall()))

    def update(self, data=[]):
        print(data)
        query = 'INSERT INTO temperature (value, timestamp) VALUES'
        for entry in data: query += ' (%s, "%s")' % (entry['value'], entry['timestamp'])
        query += ';'

        print(query)

        result = self.conn.execute(query)
        self.conn.commit()
        print(result)
        return result
