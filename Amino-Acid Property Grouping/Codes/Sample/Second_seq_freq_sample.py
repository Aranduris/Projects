"""
This code was meant to obtia secondary strucure infomraiton from our sample data
"""

import pandas as pd
# Function to count amino acids in a sequence
def count_ss(sequence):
	length_seq = len(sequence)
	ss_count = {}
	for ss in sequence:
		if ss in ss_count:
			ss_count[ss] += 1
		else:
			ss_count[ss] = 1

	ss_freq = {key: round(value / length_seq,4) for key, value in ss_count.items()}
	return ss_freq

df = pd.read_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/sample/secondary_struct.csv')

# Apply the count_amino_acids function to each sequence in the DataFrame
df['second_s_freq'] = df['sec_seq'].apply(count_ss)

# Convert the amino_acid_freq column into a DataFrame
a_ss_freq_df = pd.DataFrame(df['second_s_freq'].tolist())


# Calculate the mean for each amino acid
a_ss_freq = a_ss_freq_df.mean()
a_ss_freq = pd.DataFrame(list(a_ss_freq.items()), columns=['Secondary_Struct', 'Frequency'])


# Save data for Tablue
a_ss_freq.to_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/sec_s_freq_avg.csv',index=False)