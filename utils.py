import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine
import csv


def display_data_model():
    """
    Load and display image
    """
    try:
        
        img = mpimg.imread('yanki_data_model.drawio.png')
        plt.figure(figsize=(8, 6))
        plt.imshow(img)
        plt.axis('off')
        plt.title('Data Model')
        plt.show()
    except FileNotFoundError:
        print("Image file not found")
    except Exception as e:
        print('An Error occur while displaying the image', e)
    
    
def save_to_csv(dataframe: dict, folder="dataset/clean_data"):
    
    try:
        for name, df in dataframe.items():
            path = f"{folder}/{name}.csv"
            df.to_csv(path, index=False)
            print(f"{name} saved successfully to path:{path}")
    except Exception as e:
        print("Error Saving {name}.csv ", e)
        
        
def db_connection(dbname='postgres'):
    
    try:
        env_path = Path.cwd()/'.env'
        if not env_path.exists():
            print(".env file not found")
        else:
            load_dotenv(env_path)
            
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=dbname,
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            )
        return connection
    except Exception as e:
        print("Something went wrong ")
        
    
def create_database(dbname='yanki_ecommerce'):
    """ Create the target database if it does not exists"""
    
    try:
        con = db_connection('postgres')
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        
        #cursor.execute(f'SELECT 1 FROM pg_database WHERE datname={dbname}')
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
        available = cursor.fetchone()
        
        if not available:
            query = "CREATE DATABASE yanki_ecommerce"
            cursor.execute(query)
            print(f"{dbname} database created successfully")
        else:
            print("Database already exists")
        cursor.close()
        con.close()
    except Exception as e:
        print("Error while creating database", e)
        

def create_tables(schema_path="schema.sql", dbname="yanki_ecommerce"):
    """ Execute all SQL Query from schema file to create tabled"""
    try:
        with open(schema_path, 'r') as file:
            query = file.read()
        
        con = db_connection(dbname)
        cursor = con.cursor()
        
        cursor.execute(query)
        con.commit()
        cursor.close()
        con.close()
        
        print("Tables created successflly")
    except Exception as e:
        print("Error occur while creating tables...", e)
        
    
def get_engine(dbname='yanki_ecommerce'):
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = dbname
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(DATABASE_URL)


def load_data_from_df(dataframe):
        
    try:
        engine = get_engine()
        for name, df in dataframe.items():
            df.to_sql(name, engine, if_exists='append', index=False)
            print(f"Data loaded to table '{name}' successfully.")
    except Exception as e:
        print(f"Error creating table {name}:", e)
        
        
# def load_data_from_csv(csv_file, dbname='yanki_ecommerce'):
#     con = db_connection(dbname)
#     cursor = con.cursor()
#     with open(csv_file, 'r') as file:
#         reader = csv.reader(file)
#         next(reader)
#         for row in reader:
#             cursor.execute()