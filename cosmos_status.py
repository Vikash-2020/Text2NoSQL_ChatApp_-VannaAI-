from app_secrets import  cosmos_db_api_key, cosmos_db_url
from azure.cosmos import CosmosClient
import datetime


def connect_to_db():
    url = cosmos_db_url
    key = cosmos_db_api_key
    database_name = 'Userdb2'
    container_name = 'user_data'

    database_client = CosmosClient(url, credential=key)
    database = database_client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return container

def connect_and_query_db(container, db_query):  
    try:  
        items = list(container.query_items(  
            query=db_query,   
            enable_cross_partition_query=True  
        ))
        return items

    except Exception as e:  
        print(f"Error occurred: {e}")  
        return None

def db_info():
    container = connect_to_db()
    total_entries = connect_and_query_db(container, "SELECT VALUE COUNT(1) FROM c")
    persona_list = ['Knowledge Asst', 'Writing Asst', 'Grammar Asst', 'Technical Asst', 'Summarizing Asst']
    name_list = connect_and_query_db(container, "SELECT DISTINCT VALUE q.userName FROM c JOIN q IN c.questions")
    email_list = connect_and_query_db(container, "SELECT DISTINCT VALUE c.email FROM c")

    return {"total_database_entries": total_entries, "persona_list": persona_list, "username_list": name_list, "email_list": email_list}

db_status = db_info()
current_datetime = datetime.datetime.now()

def get_latest_db_info():
    latest_db_status = f"""Latest Information from Database, Updated at current datetime: {current_datetime}\n---\n"""+"""Database Schema:\n```json  \n{    \n    \"id\": \"string\",    \n    \"email\": \"string\",    \n    \"timestamp\": \"date\",    \n    \"questions\": [    \n        {    \n            \"userName\": \"string\",    \n            \"questionType\": \"string\",    \n            \"userQuestion\": \"string\",    \n            \"personna\": \"string\"    \n        }    \n    ]    \n}  \n```  \n"""+f"""\n \nTotal Database Entries: {db_status['total_database_entries']}\n\nList of `personna`: {db_status['persona_list']}\n\nList of `userName`: {db_status['username_list']}\n\nList of `email`: {db_status['email_list']}\n---\n\nThis is the latest info provided by database. Use this information to generate database query or further response."""
    
    return latest_db_status
    


    
