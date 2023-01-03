To run the app:\
cd to where Main.py is\
set FLASK_APP = Main.py\
flask run

File Map:
+ Data_Backup
  - The folder contains the xml and txt files that were processed and scraped from various websites.
+ Other_Scripts
  - Folder contains various python and R scripts that were utilized to construct the data base.
+ Static
  - Contains the css file that was used to style the database website
+ Templates
  - Folder holds the raw coded HTML code for the database website
+ config
  - Connects the database to the server
+ Documentation
  - Describes what the database is all about and how the database was constructed. 
+ Graphs.py
  - Python file that was used to create plots
+ Main.py
  - Initializes and constructs the database website. Also the file that launches the flask application i.e. the database
+ Queries.py
  - The various SQL queries called for the database.
