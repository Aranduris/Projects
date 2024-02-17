########################## Do not run this file first! ########################
# You will need to download obonet libraby. Its just 'pip install obonet'
# Make sure to change/ provide your own path for the file otherwise the file won't work

import pandas as pd
import obonet
import mysql.connector

# Make sure the chnage the path name apropriate to where the file is within your system

graph = obonet.read_obo('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/go-basic.obo')
# Extract node attributes
node_data = []
for node, data in graph.nodes(data=True):
	data['id'] = node
	node_data.append(data)

# Convert to DataFrames
node_df = pd.DataFrame(node_data)

# Convert tsv file into a data frame
go_conn = pd.read_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/terms.tsv',
						 sep='\\t', engine='python')

# Make sure to only obtain the neccessary infromation we don't really need the rest
Feature_recs = pd.DataFrame()
Feature_recs["Id"] = node_df['id']
Feature_recs["Feature"] = node_df['name']

# I dropped the last column called aspect I wasn't sure what that was about. 
go_conn = go_conn.iloc[:,0:2]

# Connects to SQL
mydbase = mysql.connector.connect(host="localhost", user="root", passwd="1234")
mycursor = mydbase.cursor()

# Drops tables if they already exist.
mycursor.execute("USE CAFA")
mycursor.execute("""DROP TABLE if EXISTS Go_seqs;""")
mycursor.execute("""DROP TABLE if EXISTS Go_Functions;""")

# Create the third table
# Go_Functions(go_id, go_function)
mycursor.execute("""CREATE TABLE Go_Functions (
  					go_id VARCHAR(100) NOT NULL,
  					go_function TEXT NOT NULL,
  					PRIMARY KEY (go_id));""")
mydbase.commit()

for index,row in Feature_recs.iterrows():
    mycursor.execute("INSERT INTO CAFA.Go_Functions(go_id,go_function) VALUES (%s,%s)", 
                     (row['Id'],row['Feature']))
mydbase.commit()

# Create the fourth table
# Go_Seqs(go_seq_id,go_go_id)
mycursor.execute("""CREATE TABLE Go_Seqs (
  					go_seq_id VARCHAR(100) NOT NULL,
  					go_go_id  VARCHAR(100) NOT NULL,
  					PRIMARY KEY (go_seq_id,go_go_id),
  					FOREIGN KEY (go_seq_id) REFERENCES Sequence(seq_id) ON DELETE CASCADE,
  					FOREIGN KEY (go_go_id) REFERENCES Go_Functions(go_id));""")
mydbase.commit()

for index,row in go_conn.iterrows():
    mycursor.execute("INSERT INTO CAFA.Go_Seqs(go_seq_id, go_go_id) VALUES (%s,%s)", 
                     (row['EntryID'], row['term']))
mydbase.commit()

mycursor.close()
mydbase.close()