#Sends queries to the database to recieve infomration
import psycopg2
import pandas as pd
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
#Get all data from plants
def get_plants():
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM Plants')
        for d in cursor:
            yield d
#Get all data from viruses
def get_viruses():
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM Viruses')
        for d in cursor:
            yield d
#Get Just the scientifc name and virus name from infects
def get_infects():
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute('SELECT scientificname,virusname FROM Infect')
        for d in cursor:
            yield d
#Get all data from the CDS as well as the virus table.
#To display the name of the virusID
def get_CDS():
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM cds JOIN viruses ON  cds.virusid = viruses.id')
        for d in cursor:
            yield d
#Get all data from the motifs_domain
def get_motifs_domain():
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM CDSresult\
                        JOIN cds ON cdsresult.cdsuniqueid  = cds.cdsid\
                        JOIN viruses ON  cds.virusid = viruses.id')
        for d in cursor:
            yield d
#Returns the plant the user searched for using scientific name
def search_scientific(search):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM infect\
                        JOIN Viruses ON infect.virusname = Viruses.name\
                        JOIN CDS ON Viruses.id = CDS.virusid\
                        JOIN CDSresult ON CDS.cdsid = CDSresult.cdsuniqueid\
                        WHERE scientificname = %s', (search,))
        for d in cursor:
            yield d
#Returns the plant the user searched for using common name
def search_full(search):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM plants\
                        JOIN Infect ON plants.scientificname = Infect.scientificname\
                        JOIN Viruses ON infect.virusname = Viruses.name\
                        JOIN CDS ON Viruses.id = CDS.virusid\
                        JOIN CDSresult ON CDS.cdsid = CDSresult.cdsuniqueid\
                        WHERE commonname = %s', (search,))
        for d in cursor:
            yield d
#Returns the plant the user searched for using virus name
def search_virus(search):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM Viruses\
                        JOIN CDS ON Viruses.id = CDS.virusid\
                        JOIN CDSresult ON CDS.cdsid = CDSresult.cdsuniqueid\
                        WHERE name = %s', (search,))
        for d in cursor:
            yield d
#Returns the plant the user searched for using motif name
def search_motif(search):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM CDSresult\
                        JOIN CDS ON CDSresult.cdsuniqueid = CDS.cdsid\
                        JOIN Viruses ON CDS.virusid = viruses.id\
                        WHERE motifname = %s', (search,))
        for d in cursor:
            yield d