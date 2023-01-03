#Create tables and populates them
import csv
import psycopg2
import psycopg2.extras
from urllib.parse import urlparse, uses_netloc
import configparser
#initalize connection to the database
def connect_to_db(conn_str):
    uses_netloc.append('postgres')
    url = urlparse(conn_str)

    conn = psycopg2.connect(database=url.path[1:],
                            user=url.username,
                            password=url.password,
                            host=url.hostname,
                            port=url.port)

    return conn
#Load connection infomration from Config.ini
config = configparser.ConfigParser()
config.read('config.ini')
connection_string = config['database']['postgres_connection']
conn = connect_to_db(connection_string)
cursor = conn.cursor()
#Create the tables and columns

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Plants (ScientificName VARCHAR(255) NOT NULL, CommonName VARCHAR(255) NOT NULL, 
    PRIMARY KEY(ScientificName))
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Infect (Infection_ID VARCHAR(20) NOT NULL, ScientificName VARCHAR(255) NOT NULL, 
    VirusName VARCHAR(255) NOT NULL , PRIMARY KEY(Infection_ID), 
    FOREIGN KEY (ScientificName) REFERENCES Plants(ScientificName)
    ON DELETE CASCADE ON UPDATE CASCADE 
    DEFERRABLE INITIALLY DEFERRED)
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Viruses (Name VARCHAR(255) NOT NULL, ID INTEGER NOT NULL,
    Sequence TEXT, PRIMARY KEY (ID))
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS CDS (VirusID INTEGER NOT NULL, CDSID VARCHAR(20) NOT NULL, CDSStart INTEGER,
    CDSStop INTEGER, CDSTranslatedSeq TEXT, PRIMARY KEY (CDSID),
    FOREIGN KEY (VirusID) REFERENCES Viruses(ID)
    ON DELETE CASCADE ON UPDATE CASCADE
    DEFERRABLE INITIALLY DEFERRED)
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS CDSResult (CDSResultID VARCHAR(20) NOT NULL, CDSUniqueID VARCHAR(20) NOT NULL,
    MotifStart INTEGER, MotifStop INTEGER, EValue DOUBLE PRECISION, BitScore DOUBLE PRECISION,
    AccessionNo VARCHAR(50), MotifName VARCHAR(225), PRIMARY KEY (CDSResultID),
    FOREIGN KEY (CDSUniqueID) REFERENCES CDS(CDSID)
    ON DELETE CASCADE ON UPDATE CASCADE
    DEFERRABLE INITIALLY DEFERRED)
""")
#Insert the data into the tables
with open('Plants.csv', 'r') as Plants:
    reader = csv.reader(Plants)
    for row in reader:
        cursor.execute('INSERT INTO Plants VALUES (%s,%s)',row)

with open('Infect.csv', 'r') as Infects:
    reader = csv.reader(Infects)
    for row in reader:
        cursor.execute('INSERT INTO Infect VALUES (%s,%s,%s)',row)

with open('Viruses.csv', 'r') as Viruses:
    reader = csv.reader(Viruses)
    for row in reader:
        cursor.execute('INSERT INTO Viruses VALUES (%s,%s,%s)',row)

with open('CDS.csv', 'r') as CDS:
    reader = csv.reader(CDS)
    for row in reader:
        cursor.execute('INSERT INTO CDS VALUES (%s,%s,%s,%s,%s)',row)

with open('CDS_Motifs.csv', 'r') as CDS_Motifs:
    reader = csv.reader(CDS_Motifs)
    for row in reader:
        cursor.execute('INSERT INTO CDSResult VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',row)
# Commit and close the connection after the queries
conn.commit()
conn.close()