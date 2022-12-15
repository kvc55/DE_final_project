## About the Project
This project was a direct request from the CEO's secretary.
We were asked to develop a technological solution for management decision-making using the datadriven concept.

To do this, access to the documents used by various areas of the company was requested. It was possible to catalog 9 csv documents, of which **8 could be used for this development**.

### What was developed:
- A web platform for online consultation of said documents with a friendly graphical environment for the end user
- A database in PostgresSQL
- A class in python to communicate with the database and methods that allow to execute dynamic queries without requiring great knowledge in SQL
- A bank of views of SQL queries
- Notebooks with data analysis of the obtained dataset


To populate the database, modules were designed in python that execute a CSV transformation process for later use.

----------------------------------------------

### Repository map:

**/app** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;< folder: contains backend files.  
**/data** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;< folder: contains uploaded CSV and fetchable datasets.  
**/db** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;< folder: contains SQL files.  
**/docs/txt**  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;< folder: contains test results in TXT format.  
**/frontend**         &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;< folder: contains Streamlit and FastAPI files and log config.  
**/notebooks**        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;< folder: contains Jupyter Notebook.  
**/src**              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;< folder: contains Python modules for DB methods and ETL.  
**/temp**              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;< folder: contains temporary files with module outputs.      
**main.py**           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;< file  : Python file to execute all the steps to populate the ddbb.   
**requeriments.txt**  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;< file: has all the Python required packages to install.   
**README.md**         &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;< file  : contains use instructions.  

-----------------------
**/frontend/logsetup/**    &nbsp;< folder : contains logging configuration.  
**/frontend/pages**        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;< folder : contains Streamlit Python files. 

-----------------------
**/apps/back/api**    &nbsp;< folder : Python API module. Sets endpoints for uploading and fetching data.  

-----------------------
**/db/create_tables.sql**  &nbsp;&nbsp;&nbsp;< file: SQL scripts to create the DB.     
**/db/insight_querys.sql** < file: insight SQL queries.   
**/db/create_views.sql**   &nbsp;&nbsp;&nbsp;< file: SQL scripts to create views.   

-----------------------
**/notebooks/eda_prechecks.ipynb**     &nbsp;&nbsp;&nbsp;< file: Jupyter Notebook with the analysis done to the CSV files before database creation to understand the data on those files.  
**/notebooks/ddbb_analysis.ipynb**     &nbsp;&nbsp;&nbsp;&nbsp;< file: Jupyter Notebook with analysis done to decide the databse structure.  
**/notebooks/insights_analysis.ipynb** < file: Jupyter Notebook with partial insights, analysis and useful information.

-----------------------
**/src/dbmodules.py**   < file: Python file with class and methods for DB connection and manipulation.   
**/src/etl_to_db.py**   &nbsp;&nbsp;&nbsp;< file: Python file with functions to execute the CSV loading and the data transformation.  


# Installation
1) Create a [Python virtual enviroment using venv](https://docs.python.org/3/library/venv.html) (Python >3.x required)

## Activate venv:
`source bin/activate` (in Ubuntu)

## Install requirements:
`pip install -r requirements.txt`

<br>

# Execution

### (FastAPI) Run in the local server: 
`uvicorn api:app --reload`

### (Streamlit) Run in the instance: 
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
