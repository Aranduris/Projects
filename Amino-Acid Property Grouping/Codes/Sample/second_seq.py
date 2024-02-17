"""
This code processed the raw secondary strucure files 
obtained after running s4pred into a
singular file for easier data analysis and applications 
for machine learning
"""

import pandas as pd
import os

# 
path = 'C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/s4pred_preds/'

main = []

# For file in the folder
for filename in os.listdir(path):
    # if the filename ends with .fas
    if filename.endswith('.fas'):
        # Create a new path with the name of the file
        file_path = os.path.join(path, filename)
        # Open that file based on the new path
        with open(file_path, 'r') as file:
            # Extract data into a list of lists
        	lines = file.read().split('\n')
        	temp = []
        	for line in lines:
        		temp.append(line)
        	main.append(temp)
# Initialize a data frame from the list of lists
df = pd.DataFrame(main, columns=['Column1', 'Column2', 'Column3', 'Column4'])
# Drop un-nessary coloumns
df = df.drop(columns=['Column2','Column4'])
# Fix the strings such that ">" is no long part of the string 
df['Column1'] = df['Column1'].apply(lambda x: x.split(">")[1].strip())

# Rename the columns appropraitly
column_name_mapping = {'Column1': 'sec_seq_id','Column3': 'sec_seq'}
df = df.rename(columns=column_name_mapping)
# same data
df.to_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/sample_break/secondary_struct.csv')