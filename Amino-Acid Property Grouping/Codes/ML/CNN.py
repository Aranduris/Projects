# Base Imports
import numpy as np
from numpy import asarray
import pandas as pd
import os

# Train test split and performance measures
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score,accuracy_score

# class balancing
from sklearn.utils.class_weight import compute_sample_weight

# Image creating and Processing
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from PIL import Image

# CNN
from functools import partial
import tensorflow as tf
from tensorflow.keras import datasets, layers, models

# Obtain Names for each funtion
Names = pd.read_csv("C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/Sample/sample_function.csv")
Names = Names.drop('t_tax_seq_id', axis=1)
Names = Names.drop_duplicates()

# Make sure only the ten functions that we aimed to look at in the study are selected
Function = pd.read_csv("C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/Sample/sample_function.csv")
Function = Function.drop('go_function',axis=1)
final_table_columns = ['GO:0008150','GO:0005488','GO:0003824','GO:0005515',
                       'GO:0005575','GO:0008152','GO:0009987','GO:0003674',
                       'GO:0110165','GO:0071704']
Function = Function[Function['go_go_id'].isin(final_table_columns)]

# One hot encoded the functions for easier classification 
one_hot_encoded = pd.get_dummies(Function, columns=['go_go_id'])
one_hot_encoded = one_hot_encoded.groupby('t_tax_seq_id').sum().reset_index()
one_hot_encoded.columns = one_hot_encoded.columns.str.replace('go_go_id_', '')

# Read in sequence data
Seq = pd.read_csv("C:/Users/ritwi/OneDrive/Documents/MS_DataScience/Thesis/Project/Data/Sample/sample.csv")
Seq = Seq.drop('tax_id',axis=1)

# merge the sequence data with the function data on the sequence id
Merge_df = pd.merge(Seq, one_hot_encoded, left_on='tax_seq_id', right_on='t_tax_seq_id', how='inner')

# merge the columsn and reset the index
Merge_df = Merge_df.drop(columns=['t_tax_seq_id'])
Merge_df.set_index('tax_seq_id', inplace=True)
Merge_df['seq_length'] = Merge_df['seq'].apply(lambda x: len(str(x)))
Merge_df = Merge_df[Merge_df['seq_length']<=500]
Merge_df = Merge_df.drop(columns=['seq_length'])

# Split the data into X and Y variables
X = Merge_df.drop(columns=Merge_df.columns[1:])
Y = Merge_df.drop(columns=Merge_df.columns[0])

# Obtain the images data
X_image = np.empty((2312,28, 28, 4))
for i in range(0,2312):
    img = Image.open(f'Heatmaps/{i}.png')
    numpydata = asarray(img)
    X_image[i] = numpydata

# Use the images and Y data and perform an 80-20 split
X_train, X_test, y_train, y_test = train_test_split(X_image, Y, test_size=0.2)

# Generate the CNN model that was used for this study
model = models.Sequential()
model.add(layers.Conv2D(28, (4, 4), activation='tanh', input_shape=(28, 28, 4)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (4, 4), activation='tanh'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(28, (4, 4), activation='tanh'))
model.add(layers.Flatten())
model.add(layers.Dense(16, activation='tanh'))
model.add(layers.Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adadelta',metrics=[tf.keras.metrics.BinaryAccuracy()])

# Run the model for different function and obtain the F1-Score and Accuracy
Records = pd.DataFrame(columns=['Go-Ids', 'F1-Score','Accuracy'])
for column in y_train.columns:
    temp = []
    a = y_train[column]
    b = y_test[column]
    sample_weights = compute_sample_weight(class_weight='balanced', y=a)
    history = model.fit(X_train,a,epochs=10,sample_weight=sample_weights)
    y_pred = model.predict(X_test)
    y_pred = [0 if value < 0.5 else 1 for value in y_pred]
    temp.append(column)
    temp.append(f1_score(b, y_pred, average='binary'))
    temp.append(accuracy_score(b,y_pred))
    Records.loc[len(Records)] = temp

# Simply processing the data a little more for easier analysis.
Records = Records.merge(Names, left_on='Go-Ids', right_on='go_go_id')
Records = Records.drop(columns=['go_go_id'])
Records =  Records.iloc[:,[0,3,1,2]]
Records =  Records.sort_values(by=['F1-Score','Accuracy'], ascending=False)
print(Records)