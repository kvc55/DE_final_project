The project was a request from the CEO's secretary.
We were asked to develop a technological solution for management decision-making using the datadriven concept.

To do this, access to the documents used by various areas of the company was requested. It was possible to catalog 9 csv documents, of which 8 could be used for this development.

We developed:
- A web platform for online consultation of said documents with a friendly graphical environment for the end user
- A database in PostgresSQL
- A class in python to communicate with the database and methods that allow to execute dynamic queries without requiring great knowledge in SQL
- A bank of views of SQL queries
- Notebooks with data analysis of the obtained dataset


To populate the database, modules were designed in python that execute a CSV transformation process for later use.

----------------------------------------------

Repository map:

/db               < folder: contains sql files
/frontend         < folder: contains streamlit/fastapi files and logging configuration
/notebooks        < folder: contains jupyter notebooks
/src              < folder: contains .py modules 
README.md         < file  : contains use instructions 
main.py           < file  : python file to execute all the steps to populate the ddbb 
requeriments.txt  < file: has all the python required packages to install


/frontend/logsetup/    < folder : contains logging configuration
/frontend/pages        < folder : contains streamlit python files




-----------------------
/db/create_tables.sql  < file: Sql scripts to create the ddbb 
/db/insight_querys.sql < file: usefull sql querys to use
/db/create_views.sql   < file: Sql scripts to create the views

-----------------------
/notebooks/eda_prechecks.ipynb     < file: jupyter notebook with the analysis done to the CSV files before of the ddbb creation to understand the data on those files
/notebooks/ddbb_analysis.ipynb     < file: jupyter notebook with the analysis done to decide the ddbb structure
/notebooks/insights_analysis.ipynb < file: jupyter notebook with partial insights analysis and some other usefull information

-----------------------
/src/dbmodules.py   < file: python file with class and methods for ddbb connection and manipulation  
/src/etl_to_db.py   < file: python file with functions to execute the csv loading and the data transformations


-------- INSTALATION PROCEDURE ---------------
1) Create a python virtual enviroment (required python 3.9)

Installation
## Activate venv:
`source bin/activate` (in Ubuntu)

## Install requirements:
`pip install -r requirements.txt`

<br>

# Execute
### Move to the /page folder: 
`cd page`

### (FastAPI) Run in the local server: 
`uvicorn api:app --reload`

### (Streamlit) Run in the l: 
`streamlit run main_page.py`

2) Create database
 - Install PostgresSQL database ver. 15.1
 The configuration for this project uses postgres user as owner of all the resources.
 Please refer to: https://www.postgresql.org/download/
 - Use /db/create_tables.sql to create the database and the tables
 - Use /db/create_views.sql to create the views

3) Upload csv files using web interface
 - Also each file can be reviewed and analysed online using the web interface

4) Run main.py to populate the database
Please refer to /src/dbmodules.py file to check all the methods that can been used with the database.
