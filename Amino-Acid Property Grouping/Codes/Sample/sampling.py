"""
This file obtains the sample sequence data long with the function-id and sequnece.
"""

import pandas as pd
import mysql.connector

df = pd.read_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/sample.csv')

df = df.rename(columns={'tax_id': 't_tax_id', 'tax_seq_id': 't_tax_seq_id', 'seq':'t_seq'})

# Connects to SQL
mydbase = mysql.connector.connect(host="localhost", user="root", passwd="1234")
mycursor = mydbase.cursor()
# Drops tables if they already exist.
mycursor.execute("USE CAFA")



#data = ("""WITH single_tax_seqs AS(
#		   SELECT tax_id, tax_seq_id
#		   FROM (
#			  SELECT tax_id, tax_seq_id,
#				  ROW_NUMBER() OVER (PARTITION BY tax_id ORDER BY RAND()) AS rn
#		   FROM taxonomy
#		   ) AS ranked
#		   WHERE rn = 1)
#
#		   SELECT single_tax_seqs.tax_id, single_tax_seqs.tax_seq_id, sequence.seq
#		   FROM sequence
#		   JOIN single_tax_seqs ON sequence.seq_id = single_tax_seqs.tax_seq_id;""")
#
#dat = pd.read_sql(data,mydbase)
#mycursor.close()
#mydbase.close()

#dat.to_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/sample.csv',index=False)


data = ("""SELECT sample.t_tax_seq_id, go_seqs.go_go_id, go_functions.go_function
		   FROM sample
		   JOIN go_seqs ON sample.t_tax_seq_id = go_seqs.go_seq_id
		   JOIN go_functions ON go_seqs.go_go_id = go_functions.go_id;""")
dat = pd.read_sql(data,mydbase)
mycursor.close()
mydbase.close()

dat.to_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/sample_function.csv')