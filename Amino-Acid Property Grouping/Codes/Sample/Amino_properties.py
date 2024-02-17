"""
Applicaiton of our property grouping technique.
Converts a standard sequence into the property grouping sequence. 
"""

import pandas as pd

# Function to count amino acids in a sequence
def get_aa_prop(sequence):
	mapping = {'A': 'A', 
			   'I': 'A',
			   'L': 'A',
			   'M': 'A',
			   'V': 'A',
			   'F': 'R',
			   'W': 'R',
			   'Y': 'R',
			   'N': 'P',
			   'C': 'P',
			   'Q': 'P',
			   'S': 'P',
			   'T': 'P',
			   'D': 'C',
			   'E': 'C',
			   'R': 'B',
			   'H': 'B',
			   'K': 'B',
			   'G': 'U',
			   'P': 'U',
			   'O': 'S',
			   'U': 'S',
			   'Z': 'S'}
	output_prop = ''.join([mapping.get(letter, letter) for letter in sequence])
	return output_prop
    	
# Reads the sample sequences
df = pd.read_csv("C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/Sample/seq_sample.csv", sep=",")
prop = []

# For every seqeunce apply the property grouping 
for index, row in df.iterrows():
	sequence = row['seq']
	prop.append(get_aa_prop(sequence))

# create a new dataframe with the grouping data
df_new = pd.DataFrame({'id': df['id'], 'amino_prop': prop})
# Save the new dataframe 
df_new.to_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/Sample/Amino_prop.csv',index=False)
