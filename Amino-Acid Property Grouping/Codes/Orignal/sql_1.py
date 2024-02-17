# Run this file first! 
# You will need to download Bio. Its just 'pip install Bio'
# Make sure to change/ provide your own path for the file otherwise the file won't work 


from Bio import SeqIO
import pandas as pd
import mysql.connector

# Open file and get the sequence id and sequence itself
with open('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/sequences.fasta') as fasta_file:
	# Creates two lists with those records
	ids = []
	seq = []
	for seq_record in SeqIO.parse(fasta_file, 'fasta'):
		ids.append(seq_record.id)
		seq.append(str(seq_record.seq))

# converts the tsv file into a data frame
tax_conn = pd.read_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/taxonomy.tsv',
						 sep='\\t', engine='python')

# Adds the list created to a data frame
Sequenc_recs = pd.DataFrame()
Sequenc_recs["Id"] = ids
Sequenc_recs["Seq"] = seq

# Connects the SQL server
mydbase = mysql.connector.connect(host="localhost", user="root", passwd="1234")
mycursor = mydbase.cursor()

# Creates a new data base
mycursor.execute("DROP DATABASE IF EXISTS CAFA")
mycursor.execute("CREATE DATABASE CAFA")
mycursor.execute("USE CAFA")

# Adds the first table 
# Sequence(seq_id(PK), seq)
mycursor.execute("""CREATE TABLE Sequence (
  					seq_id VARCHAR(100) NOT NULL,
  					seq TEXT NOT NULL,
  					PRIMARY KEY (seq_id));""")
mydbase.commit()

for index,row in Sequenc_recs.iterrows():
    mycursor.execute("INSERT INTO CAFA.Sequence(seq_id,seq) VALUES (%s,%s)", 
                     (row['Id'],row['Seq']))
mydbase.commit()

# Adds the second table
# Taxonomy(tax_seq_id, tax_id)

mycursor.execute("""CREATE TABLE Taxonomy (
  					tax_seq_id VARCHAR(100) NOT NULL,
  					tax_id  INT NOT NULL,
  					PRIMARY KEY (tax_seq_id,tax_id),
  					FOREIGN KEY (tax_seq_id) REFERENCES Sequence(seq_id) ON DELETE CASCADE);""")
mydbase.commit()

for index,row in tax_conn.iterrows():
    mycursor.execute("INSERT INTO CAFA.Taxonomy(tax_seq_id, tax_id) VALUES (%s,%s)", 
                     (row['EntryID'], row['taxonomyID']))
mydbase.commit()
mycursor.close()
mydbase.close()