import psycopg2
import pandas as pd
import configparser
import matplotlib.pyplot as plt
from urllib.parse import urlparse, uses_netloc
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
#set the connection to the database
config = configparser.ConfigParser()
config.read('config.ini')
connection_string = config['database']['postgres_connection']
conn = connect_to_db(connection_string)
cursor = conn.cursor()
#call query for the table needed to make the graph
cursor.execute('SELECT scientificname FROM Infect')
data = cursor.fetchall()
#close connection
cursor.close()
conn.close()

################### create graph #####################
# make graph
df = pd.DataFrame(data)
x = df[0].value_counts()
graph = x.plot.bar(title= 'X = Plant vs Y = Known Infections Viruses', color=(0.2, 0.4, 0.6, 0.6))
#tuns off x-axes and labels for x and y axis
axl = plt.axes()
x_axis = axl.axes.get_xaxis()
x_axis.set_visible(False)
#Saves the graph as a png
fig = graph.get_figure()
fig.savefig('graph1.png',dpi=600)