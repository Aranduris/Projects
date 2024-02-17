"""
This code serves to find the amino acid frequency distribution
"""

import pandas as pd

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


seq_sample = pd.read_csv("C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/Sample/seq_sample.csv", sep=",")

# Apply the count_amino_acids function to each sequence in the DataFrame
seq_sample['amino_acid_freq'] = seq_sample['seq'].apply(count_amino_acids)

# Convert the amino_acid_freq column into a DataFrame
amino_acid_freq_seq_sample = pd.DataFrame(seq_sample['amino_acid_freq'].tolist())


# Calculate the mean for each amino acid
average_amino_acid_freq = amino_acid_freq_seq_sample.mean()
average_amino_acid_freq = pd.DataFrame(list(average_amino_acid_freq.items()), columns=['Amino_Acid', 'Frequency'])


# Save data for Tablue
#average_amino_acid_freq.to_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/Sample/mean_sample_freq.csv',index=False)


#Droping Seq Column
seq_sample = seq_sample.drop('seq', axis=1)

# Convert dictionaries to columns
freq_sample = pd.DataFrame(seq_sample['amino_acid_freq'].apply(pd.Series))

# Rename columns if needed
freq_sample = freq_sample.rename(columns=lambda x: f'{x}')

freq_sample = freq_sample.join(seq_sample)

freq_sample = freq_sample.drop('amino_acid_freq', axis=1)

cols = ['id','M', 'N', 'A', 'Q', 'K', 'S', 'I', 'L', 'V', 'T', 'G', 'C', 'D', 'E',
       'P', 'Y', 'F', 'W', 'R', 'H', 'O', 'U', 'Z']

freq_sample = freq_sample[cols]

freq_sample.to_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/Sample/sample_freq.csv',index=False)
