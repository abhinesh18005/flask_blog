

import mysql.connector
from mysql.connector import errorcode

config = {
  'host':'dbms-proj-server.mysql.database.azure.com',
  'user':'dbmsproj@dbms-proj-server',
  'password':'Dbmspr0j3ct75',
  'database':'antique_store'
}

cursor

try:
    conn = mysql.connector.connect(**config)
    print("Connection established")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with the user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor = conn.cursor()
    cursor.execute("select * from categories;")
    
    print("Done.")