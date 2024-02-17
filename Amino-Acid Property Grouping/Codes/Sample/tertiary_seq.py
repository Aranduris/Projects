"""
Splits our sample data into 4 parts and then joins 
them back together after processing
"""

import pandas as pd
import re
#df = pd.read_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/sample.csv')
#df = df.drop('tax_id', axis=1)

#df1 = df.iloc[:999]
#df2 = df.iloc[999:1998]
#df3 = df.iloc[1998:2998]
#df4 = df.iloc[2998:]

#print(df1)
#print(df2)
#print(df3)
#print(df4)
#df1.to_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/sample_break/one.csv')
#df2.to_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/sample_break/two.csv')
#df3.to_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/sample_break/three.csv')
#df4.to_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/sample_break/four.csv')

# Joining

df1 = pd.read_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/Sample/sample_break/job_1_hitdata.txt', sep='\t')

df2 = pd.read_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/Sample/sample_break/job_2_hitdata.txt', sep='\t')

df3 = pd.read_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/Sample/sample_break/job_3_hitdata.txt', sep='\t')

df4 = pd.read_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/Sample/sample_break/job_4_hitdata.txt', sep='\t')

frames = [df1, df2, df3, df4]
df = pd.concat(frames)
df.reset_index(drop=True)

df['Query'] = df['Query'].apply(lambda x: x.split("- >")[1].strip())

df.to_csv('C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/Sample/tertiary_struct.csv')