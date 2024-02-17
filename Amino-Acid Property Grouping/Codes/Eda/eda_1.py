import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

# Function to count amino acids in a sequence
def count_amino_acids(sequence):
	length_seq = len(sequence)
	amino_acids_count = {}
	for amino_acid in sequence:
		if amino_acid in amino_acids_count:
			amino_acids_count[amino_acid] += 1
		else:
			amino_acids_count[amino_acid] = 1

	amino_acids_freq = {key: round(value / length_seq,4) for key, value in amino_acids_count.items()}
	return amino_acids_freq

# Connects to SQL
mydbase = mysql.connector.connect(host="localhost", user="root", passwd="1234")
mycursor = mydbase.cursor()

# Drops tables if they already exist.
mycursor.execute("USE CAFA")

join = ("""SELECT * FROM sequence;""")

df = pd.read_sql(join,mydbase)
mycursor.close()
mydbase.close()

# Apply the count_amino_acids function to each sequence in the DataFrame
df['amino_acid_freq'] = df['seq'].apply(count_amino_acids)

# Convert the amino_acid_freq column into a DataFrame
amino_acid_freq_df = pd.DataFrame(df['amino_acid_freq'].tolist())


# Calculate the mean for each amino acid
average_amino_acid_freq = amino_acid_freq_df.mean()
average_amino_acid_freq = pd.DataFrame(list(average_amino_acid_freq.items()), columns=['Amino_Acid', 'Frequency'])


# Save data for Tablue
average_amino_acid_freq.to_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/Amino_acid_freq_avg.csv',index=False)