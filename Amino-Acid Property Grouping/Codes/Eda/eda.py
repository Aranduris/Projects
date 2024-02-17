import pandas as pd
import mysql.connector

# Connects to SQL
mydbase = mysql.connector.connect(host="localhost", user="root", passwd="1234")
mycursor = mydbase.cursor()

# Drops tables if they already exist.
mycursor.execute("USE CAFA")

# Obtains the common_name, Scientific_name and Taxonomy_name form the sql server
join = ("""SELECT taxonomy.tax_id, taxon_names.sci_name, taxon_names.com_name
		   FROM taxonomy
		   JOIN taxon_names ON taxonomy.tax_id = taxon_names.taxid;""")

# Converts the data obtained from the SQL server to a dataframe
dat = pd.read_sql(join,mydbase)
mycursor.close()
mydbase.close()

# Capatalize the com_names
dat['com_name'] = dat['com_name'].str.capitalize()

# Save the data for Tablue 
dat.to_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/tax_name_done.csv',index=False)