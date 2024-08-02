"""
gxkent.py 
Kent was the city featured in the Charles Dickens classic, and is therefore the sensible name for a container of expectations
The central issue that Kent resolves is to ensure that pandas dataframes are available and populated with data
in both of our data contexts: the DataWarehouse and spark. 

TODO: 
* Command Line Support: There should actually be 2 ways to run this script against our data warehouse. One is in collab scripts.. and the other is from the command line. 
If used from the command line.. the script should seek out database credentials in the standard .env file (which should be exlcuded in .gitignore)
In fact.. the script should simply first try to find credentials from a .env file before trying to use a google drive spreadsheet to store credentials..
This will allow us to use one and only one basic "holder" for our expectations and this "holder" will hide all of the complexity of connecting..
and just allow us to think about expectations abstractly.

* Using the command line version of this script, write unit tests for this code. 
* Test should include: connecting the the DB from .env, running simple expectations that will never fail, running expectations that will always fails.. using randomly created data
to create 100 different tables that should sometimes pass and sometimes fail and then making sure that they sometimes pass and sometimes fail. 
make sure you correctly handle the case where someone tries to run the unit test without having setup .env. It should say "you need to have .env file to connect to DW" etc etc.

* Printing have easy to read colored text results. Passing tests should take no more than 1 line of text. Failing tests should take no more than three.

* Figure out how to load this as a class at the top of Google Collab Notebooks. It would suck to need this class to be included before the actual expectation tests 
while using it against the DW. The simplest way to get this to work reliably may be to "Open Source" this class and put it up on pypi so that we can just say "import kent" in google collab.
But see if there is a different way to do this consistently. It is possible to have the class just sitting next to the script in google drive... but I am afraid that 
might not be clean to support in the long term. Perhaps this should be something we contribute back to Great Expectations? I doubt they would accept it..
but we might learn alot about how GX is supposed to work when they tell us "why" they will not accept it. If we do this, we need to remove mentions of spark 
and replace them with "Spark"

The statements that I expect to see in the expectation notebooks will look like this: 

Kent = GXKent()
Kent.is_print_on_success = False

  sql_text = 
SELECT count(DISTINCT a.npi) AS new_npi_cnt
FROM default_npi_setting_count.{table_name} AS outer_table
WHERE outer_table.npi NOT IN (
    SELECT DISTINCT setting_table.npi
    FROM default_npi_setting_count.persetting_2021_12  AS setting_table
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




"""

__author__ = 'Fred Trotter'
__version__ = '0.2.1'
__date__ = '2023-12-05'


from pdb import line_prefix
import sys
import os
from importlib import util as iutil
import sqlalchemy
import pandas as pd
import great_expectations as gx
from sqlalchemy import create_engine, text
import json
from termcolor import colored
# Note, the purpose of this class is to figure out what environment it is being run in..
# which means that many of the imports are inside the class!


class GXKent(object):

    password_worksheet_default = 'DatawarehouseUP'
    is_print_on_success = True

    def __init__(self, **kwargs ) -> None:
        """
        Gives back a version of GXKent that understands how to connect to a server.
        For Google Collab: 
            kent = GXKent(password_worksheet='your_worksheet_name_here')

        For CLI:
            kent = GXKent(env_path='/where/you/put/your/.env')

        """
        self.is_CLI = False
        self.is_GC = False
        self.is_spark = False
        self.is_color_output = True
        self.expectation_dict = {}
        self.is_print_on_success = True

        self.env_path = '/var/www/Importer/.env'
        self.password_worksheet = 'DatawarehouseUP'

        #this overrides all of the critical attributes of the object with correctly named arguments..
        for key, value in kwargs.items():
            setattr(self,key,value)

        #This is where we determine if we are in a databricks or MariaDB context. 
        #The short answer is that if pyspark is available then we are in spark
        if (iutil.find_spec('pyspark')) is not None:

            self.is_spark = True
            # Then we have pyspark and we are in spark or spark simulation.
            # Lets save the spark session...  
            from pyspark.context import SparkContext
            from pyspark.sql.session import SparkSession
            sc = SparkContext.getOrCreate()

            self.spark = SparkSession(sc)
        else:
            import mysql.connector
            from dotenv import load_dotenv
            load_dotenv(self.env_path)
            # TODO This is where we sort out if we are in Google Collab or Command Line
            if os.getenv('DB_USERNAME') is not None:
                self.is_CLI = True
                # if we do not have a spark session and we are able to access a .env file we are working from the CLI 
                self.init_CLI_connection()  
            else:
                self.is_GC = True
                # if we are not in a spark session and cannot find a .env file then we are in google colab
            #Here we are in the mariadb context. 
                self.init_GC_connection()


    def init_GC_connection(self, *, gx_context_name = 'default_gx_context') -> None:
        #First we have a bunch of Google Collab specific libraries to import
        import gspread
        import getpass
        from google.auth import default #autenticating to google
        from google.colab import auth
        
        #First we use google to access a worksheet that contains your database password
        # You should NEVER save a password directly into a script, either in Colab
        # or in github.
        auth.authenticate_user()
        creds, _ = default()
        gc = gspread.authorize(creds)

        worksheet = gc.open(self.password_worksheet).sheet1 #get_all_values gives a list of rows
        rows = worksheet.get_all_values() #Convert to a DataFrame
        df = pd.DataFrame(rows)

        # Convert column first row into data column labels
        df.columns = df.iloc[0]
        df = df.iloc[1:]

        #assumes that the second row of the spreadsheet (the first row of data)
        #has the username and password, etc
        username = df.iat[0,0]
        password = df.iat[0,1]
        server = df.iat[0,2]
        port = str(df.iat[0,3])
        db = df.iat[0,4]

        # Now we have the credentials and other details we need to connect the
        # database server.

        sql_url = f"mysql+pymysql://{username}:{password}@{server}:{port}/{db}"

        engine = create_engine(sql_url)
        self.db_connection = engine.connect()
        
    def init_CLI_connection(self, *, gx_context_name = 'default_gx_context') -> None:
        user =os.getenv('GX_USERNAME')
        password =os.getenv('GX_PASSWORD')
        db = os.getenv('DB_DATABASE')
        port = os.getenv('DB_PORT')
        server = os.getenv('DB_HOST')

        sql_url = f"mysql+pymysql://{user}:{password}@{server}:{port}/{db}"

        engine = create_engine(sql_url)
        self.dataBase = engine.connect()

    #Returns a great expecations dataframe from raw SQL text
    def gx_df_from_sql(self, sql):
        #the hard work is done here.. to get a pandas dataframe
        pandas_df = self.pd_df_from_sql(sql)
        #now we convert it to great expectations
        gx_df = gx.from_pandas(pandas_df)
        #and return it.
        return(gx_df)


    #returns a pandas dataframe from raw SQL text. This is the place where spark vs Datawarehouse really matters
    def pd_df_from_sql(self, raw_text_sql):
        sqla_text = text(raw_text_sql)
        if(self.is_CLI):
            pandas_df = pd.read_sql_query(sqla_text,self.dataBase)
        else:
            if(self.is_GC):
            #Then we need to use the db_connection that we created when we initialized
            #to create the pandas dataframe. 
                pandas_df = pd.read_sql_query(sqla_text,self.db_connection)
            else:
                if(self.is_spark):
                #when we initialized we found our spark connection and now we use it to run the sql
                    spark_df = self.spark.sql(raw_text_sql)
                    pandas_df = spark_df.toPandas()
                else:
                #This means we are not in spark and we are not in the datawarehouse. This should be unreachable.
                    raise Exception("Kent.py: it should not be possible to be neither in the DataWarehouse or in spark. No .env file, worksheet, or spark instance detected.")
        return(pandas_df)    


    #this adds the results of an expectation to our list of expectation results
    def capture_expectation(self, *, expectation_name, expectation_result):
        #Is there anything else this function should be doing?
        self.expectation_dict[expectation_name] = expectation_result

    #loops over all of the expectations and prints the results
    def print_all_expectation_results(self):
        for this_name, this_result in self.expectation_dict.items():          
            self.print_one_expectation_results(
                                        expectation_name=this_name,
                                        gx_result=this_result
            )


    #this is our expectation result printer.. and it should be greatly improved. 
    def print_one_expectation_results(self, *, expectation_name, gx_result, is_print_success: bool = True):
        if """"success": false""" in gx_result.__str__():
            if self.is_color_output:
                print(colored(f"\tFAIL: {expectation_name}", 'red'))
                #print(gx_result.expectation_config)
                print(colored(gx_result.result,'red'))
            else:
                print(f"\tFAIL: {expectation_name}")
                #print(gx_result.expectation_config)
                print(gx_result.result)
        else:
            if self.is_print_on_success:
                if self.is_color_output:
                    print(colored(f"\tSUCCESS: {expectation_name}",'green'))
                else:
                    print(f"\tSUCCESS: {expectation_name}") 
