import pandas as pd
import mysql.connector

# Connects to SQL
mydbase = mysql.connector.connect(host="localhost", user="root", passwd="1234")
mycursor = mydbase.cursor()

# Drops tables if they already exist.
mycursor.execute("USE CAFA")

join = ("""SELECT go_seqs.go_seq_id AS seq_id, go_functions.go_id AS function_id, go_functions.go_function AS function_name
		   FROM go_seqs
		   JOIN go_functions ON go_seqs.go_go_id = go_functions.go_id;""")

dat = pd.read_sql(join,mydbase)
mycursor.close()
mydbase.close()

dat['function_name'] = dat['function_name'].str.capitalize()

dat.to_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/Function.csv',index=False)