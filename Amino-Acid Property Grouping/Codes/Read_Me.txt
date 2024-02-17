EDA Folder - The EDA Folder consists of code used to generate and process data.
		- eda, eda_1, eda_2, and eda_R - Files are Python and R files used to process the data for visualization. 
		- Vis_EDA is a Tableau file that generates all the visualizations.
		- Bi-Partite_Network Folder: This Folder contains the code, data, and protein Gephi file that was 
		  used to generate the network 


ML Folder - Contains the bulk of machine learning code that was written for the project. 
		- Data Folder - Contains all the variations of Data that were processed for the ML algorithms.
		- Heatmaps Folder - Contains various heatmaps that were made for each sequence for use in the CNN algorithm.
		- CNN-HeatmapGen -  Code that generates all the heatmaps from the RNN encoder.
		- CNN - Code that runs the CNN algorithm. For some reason, the algorithm wouldn't run on Jupiter notebooks and
			utilize the GPU. Hence, the network was run using a standard Python file format. 
		- ML - Code for all machine learning algorithms except CNN and RNN. 
		- Records - Excel file where the results from all the ML algorithms including CNN and RNN were processed.
		- RNN - Code to run the RNN algorithm.
		- RNN-Standard_Encoder - Code to run the RNN algorithm using a standard Encoder.


Original - This Folder is where the original data was processed and placed into a SQL server.
		- sql_1, sql_2, sql_3 - simply create tables and migrate the data to the server.
		- SQL_Playgroud - Majority of the SQL code that was used to make infernces of the data.

Sample - This folder contains all the code that was used to generate data.
		- s4pred - The application that generated the secondary structure predictions used in our study
		- Amino_Acid_Freq_sample - code for generating the amino acid frequency count within our sampled data
		- Amino_properties - The code for the property grouping data transformation
		- Sampling - The core code that generated the sample data from the original data
		- second_seq -  Processed the second_seq secondary sequence data obtained from s4pred
		- Second_seq_freq_sample - The code for frequency distribution for the secondary sequences.
		- tertiary_seq - The code to split our sample data so that the tertiary sequence information could be
				 obtained from CDD as there was a limit of only 1000 sequences per run. 
