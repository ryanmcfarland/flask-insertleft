import sqlite3
import pandas

class weaponsData(object):
    def parseFile(self):
        self.readFile('weapons.csv')

    def readFile(self, filename):
        conn = sqlite3.connect('app.db')
        df = pandas.read_csv(filename, sep="|")
        df.to_sql("weapon", conn, if_exists='append', index=False)

c = weaponsData().parseFile()