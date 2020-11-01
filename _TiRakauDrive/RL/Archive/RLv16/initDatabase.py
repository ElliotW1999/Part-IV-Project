import sqlite3
from sqlite3 import Error
import os


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        for p in range(0, 9):
            for o in range(0, 5):
                for n in range(0, 9):
                    for m in range(0, 10):
                        for i in range(0, 7):
                            for k in range(0, 9):
                                #x = format(j, '09b')
                                #x = (str(n)+str(m)+str(i)+str(k)) #remove?
                                sqlite_insert_with_param  = """INSERT INTO States (Move1, Move2, Move3, Move4, Move5, Move6, Move7) VALUES (?, ?, ?, ?, ?, ?, ?);"""
                                data_tuple = (float(1.0), float(1.0), float(1.0), float(1.0), float(1.0), float(1.0), float(1.0))
       
                                cursor.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()
        
        
        
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection(os.getcwd()+"\QTable.db")