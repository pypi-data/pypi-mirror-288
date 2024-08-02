# GXKent
A simple library that allows Great Expectations to run easily in python notebook and CLI environments

## Idea
Kent was the city featured in the Charles Dickens classic, and is therefore the sensible name for a container of expectations
The central issue that Kent resolves is to ensure that pandas dataframes are available and populated with data
in both of our data contexts: CLI and Notebooks

## Basic Usage
```
Kent = GXKent()
Kent.is_print_on_success = False

  sql_text =
SELECT count(DISTINCT a.npi) AS new_npi_cnt
FROM default_npi_setting_count.{table_name} a
WHERE a.npi NOT IN (
    SELECT DISTINCT b.npi
    FROM default_npi_setting_count.persetting_2021_12 b
    );

gxDF = Kent.gx_df_from_sql(sql_text)

Kent.capture_expectation(
    expectation_name='Between year comparision {this_year} {that_year}',
    expectation_result=gxDF.expect_column_max_to_be_between('new_npi_cnt',112671,253511)
)

Kent.capture_expectation(
    expectation_name='Between year comparision {this_year} {that_year}',
    expectation_result=gxDF.expect_column_min_to_be_between('new_npi_cnt',11671,23511)
)

Kent.capture_expectation(
    expectation_name='Between year comparision {this_year} {that_year}',
    expectation_result=gxDF.expect_column_avg_to_be_between('new_npi_cnt',50000,60000)
)
```

### CLI Usage

In order to work from the command line, there should be a .env file with database credentials in it. 
As typical .env files should be excluded in your .gitignore file. 

here is the contents expected in the .env file: 

```
GX_USERNAME=your_gx_mysql_username
GX_PASSWORD=your_gx_mysql_password
DB_DATABASE=starting_database
DB_PORT=3306
DB_HOST=localhost
```

Once your .env file has the right contents, you need to tell GXkent where it lives when you create your object with: 

```
Kent = GXKent(env_path='/where/you/put/your/.env')
```

substitute your database connection details here. 
For now, GXKent only supports MySQL. patches to use sqlalchemy properly to support other databases are welcome. 

### Google Colab Usage

In order to safely use Google Collab notebooks, it is critical to not save your password credentials in the notebook itself.
Instead you should store your credentials in a google spreadsheet and then connect your Collab notebook to that spreadsheet.

In order to use GXKent in this way, you need to pass in the credentials like so: 

```
Kent = GXKent(password_worksheet='your_worksheet_name_here')
```

Your Google Drive Spreadsheet should contain the following structure: 


| username  | password | server | port | database | 
| ------------- | ------------- | --- | --- | --- |
| your_username  | your_password | your_server | 3306 | your_database | 



## Authors
Fred Trotter and Jose Cortina
