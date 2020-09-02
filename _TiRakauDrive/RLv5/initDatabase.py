import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        
        for m in range(0, 10):
            for i in range(0, 7):
                for k in range(0, 9):
                    for j in range (0, 512):
                        x = format(j, '09b')
                        x = (str(m)+str(i)+str(k)+str(x)) #remove?
                        sqlite_insert_with_param  = """INSERT INTO States (StateID, Move1, Move2, Move3, Move4, Move5, Move6, Move7) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
                        data_tuple = (int(x), float(0), float(0), float(0), float(0), float(0), float(0), float(0))
   
                        cursor.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()
        
        
        
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection(r"C:\Users\Elliot\Documents\GitHub\P4Project\_TiRakauDrive\RL\QTable.db")