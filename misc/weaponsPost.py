from sqlalchemy import create_engine
import psycopg2
import os
import pandas

class weaponsData(object):
    def parseFile(self):
        self.readFile('misc/weapons.csv')

    def readFile(self, filename):
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = create_engine(DATABASE_URL)
        df = pandas.read_csv(filename, sep="|")
        df.to_sql("weapon", conn, if_exists='append', index=False)

c = weaponsData().parseFile()