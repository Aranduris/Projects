
import pandas as pd
import mysql.connector

# Make sure to only obtain the neccessary infromation we don't really need the rest
taxon_nam = pd.read_csv("C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/taxon_name_1.txt", sep="\t")
taxon_nam = taxon_nam.drop(columns=['Unnamed: 3', 'Unnamed: 4'])
taxon_nam['comname'] = taxon_nam['comname'].replace('character(0)', None)

# Connects to SQL
mydbase = mysql.connector.connect(host="localhost", user="root", passwd="1234")
mycursor = mydbase.cursor()

# Drops tables if they already exist.
mycursor.execute("USE CAFA")
mycursor.execute("""DROP TABLE if EXISTS taxon_names;""")

# Create table
mycursor.execute("""CREATE TABLE Taxon_names (
  					taxid VARCHAR(10) NOT NULL,
  					sci_name TEXT NOT NULL,
  					com_name TEXT,
  					PRIMARY KEY (taxid));""")
mydbase.commit()

for index,row in taxon_nam.iterrows():
    mycursor.execute("INSERT INTO CAFA.Taxon_names(taxid,sci_name,com_name) VALUES (%s,%s,%s)", 
                     (row['taxid'],row['taxname'],row['comname']))

mydbase.commit()

mycursor.close()
mydbase.close()