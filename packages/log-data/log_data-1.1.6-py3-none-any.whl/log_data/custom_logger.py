from psycopg2 import OperationalError,Error
import os
import psycopg2
import inspect
import subprocess
from datetime import datetime


from .notion import *
from custom_development_standardisation import *
from .utility import *

# from dotenv import load_dotenv
# load_dotenv()

api_key = os.getenv('api_key')
db_name = os.getenv('database_name')
db_table = os.getenv('database_table')
database_user = os.getenv('database_user')
database_host = os.getenv('database_host')
database_port = os.getenv('database_port')



class custom_logger():
    def __init__(self):
        print("Generating logger....")
        self.logging_in_progress = False
        self.storage_location = "database"
        self.notion_log_page_id = ''
        self.notion_headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        self.backup_notion_page_id = "b74cbfbe7cc2490e9dc3210f06eb3c8e"
        self.logging_table_name = db_table
        self.logging_table_columns = None
        self.connection = None
        self.client = None
    
    def change_storage_location(self):
        if self.storage_location == "notion":
            self.storage_location = "database"
        if self.storage_location == "database":
            self.storage_location = "notion"

    def test_notion_connection(self):
        outcome = get_page(self.backup_notion_page_id)
        if outcome["outcome"] == "error":
            return generate_outcome_message("error",outcome["output"],the_type=outcome["the_type"])
        return generate_outcome_message("success",outcome["output"])
    

    def initialise_database(self):
        user = database_user
        host = database_host
        port = database_port
        database_name = db_name
        table_name = db_table
        try:
            # 👀 Initialise the interface
            if user == None and host == None:
                    self.connection = psycopg2.connect(
                        database=database_name,
                        port=port,
                    )
                    self.client = self.connection.cursor()
            else:
                    self.connection = psycopg2.connect(
                        database=database_name,
                        user=user,
                        host=host,
                        port=port
                    )
                    self.client = self.connection.cursor()

            # 👀 Check if table exist
            self.client.execute("""SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema');""")
            outcome = self.client.fetchall()
            reformatted = [item[0] for item in outcome]
            exist = False
            for i in reformatted:
                if i == table_name:
                    exist = True
                    break
            if exist == False:
                return generate_outcome_message(f"{table_name} does not exist in database {database_name}...")
            
            
            # 🏃🏼‍♀️ GET COLUMNS FROM TABLE
            self.client.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
            outcome = self.client.fetchall()
            reformatted = []
            for i in outcome:
                name = i[0]
                # Remove id from the list
                if name != "id" and name != "timestamp":
                    reformatted.append(name)
                # Move time stamp to the first item in the list
            self.logging_table_columns = reformatted
            return generate_outcome_message("success",f"database reached. Primary storage location is {self.storage_location}...")
        
        # Unable to connect to database
        except OperationalError as e:
            
            # test notion connection
            outcome = self.test_notion_connection()
            if outcome == "error":
                raise RuntimeError(f"\n\nUnable to reach both psql and notion...\n\n{outcome['output']}\n\n")
            
            self.change_storage_location()
            
            return generate_outcome_message("success","Error with psql connection. Setting notion as current logging location...",the_type="others")

        
    def get_date_time(self):
        current_datetime = datetime.now().replace(microsecond=0)
        return current_datetime
    

    def store_log(self):
        # get base package information (package name, file name, function name)
        
        x = inspect.stack()
        file_path = x[1].filename
        file_name = file_path.split("/")[-1]
        outcome = get_package_name(file_path)
        if outcome["outcome"] == "error":
            raise RuntimeError(f"\n\n Failed to get package name...\n\n{outcome['output']['message']}")
        package_name = outcome["output"]
        function_name = x[1].function
        
        stringing = f"{file_name},{package_name},{function_name}"
        
        # Check state
        # location = None
        # if self.storage_location == "database":
        outcome = self.store_log_in_database(stringing)
        if outcome["outcome"] == "error" and outcome["output"]["status"] == True:
            raise RuntimeError(f"\n\nsomething went wrong with both notion and database storage...\n\n{outcome2['output']}\n\n")
        if outcome["outcome"] == "error" and outcome["output"]["status"] == False:
            self.logging_in_progress = False
            raise RuntimeError(f"\n\n something wrong with log data itself...\n\n{outcome['output']['message']}")
        # if self.storage_location == "notion":
        #     outcome = self.store_log_in_notion(stringing)
        #     if outcome["outcome"] == "error":
        #         self.logging_in_progress = False
        #         raise RuntimeError(f"\n\nsomething went wrong with both notion and database storage...\n\n{outcome['output']}\n\n")
        #     location = "notion"
        # self.logging_in_progress = False
        return generate_outcome_message("success",f"log message stored...")
        
    def store_log_in_notion(self,log_data):
        
        if self.logging_table_name == None:
            return generate_outcome_message("error","logging table name is not specified. Cannot find a logging page in notion if there is no name to compare against...",the_type="custom")
        
        # Get all the page id in the backup log page
        outcome = extract_data(self.backup_notion_page_id,data_type="page")
        
        if outcome["outcome"] == "error":
            return generate_outcome_message("error",outcome["output"],the_type=outcome["the_type"])
        
        # Go through each page, to check if there is any page with the same name as the database table where you store the logs
        page_with_logging_table_name = None
        block_id = None
        for i in outcome["output"]:
            resulting = get_page(i)
            if resulting["outcome"] == "error":
                return generate_outcome_message("error",resulting["output"],the_type=resulting["the_type"])
            if resulting["output"]["properties"]["title"]["title"][0]["text"]["content"] == self.logging_table_name:
                page_with_logging_table_name = i
                break
        
        # First time logging, create the page, create first empty block, get block id
        if page_with_logging_table_name == None:
            # Create a new page
            outcome = create_page_in_page(self.backup_notion_page_id,self.logging_table_name)
            if outcome["outcome"] == "error":
                return generate_outcome_message("error",outcome["output"],the_type=outcome["the_type"])
            page_with_logging_table_name = outcome["output"]["id"]
            # Create an empty block
            outcome = add_text_blocks(page_with_logging_table_name,[""])
            if outcome["outcome"] == "error":
                return generate_outcome_message("error",outcome["output"],the_type=outcome["the_type"])
            block_id = outcome["output"]["results"][0]["id"]
        
        # Existing page, get the first block id
        else:
            outcome = extract_data(page_with_logging_table_name,"id")
            if outcome["outcome"] == "error":
                return generate_outcome_message("error",outcome["output"],the_type=outcome["the_type"])
            array_of_block_ids = outcome["output"]
            block_id = array_of_block_ids[0]
        
        # Append current date to log
        date_appended_log = f"{self.get_date_time()},{log_data}"

        # append to the block
        outcome = append_text_to_text_block(block_id,f"\n{date_appended_log}")
        if outcome["outcome"] == "error":
            return generate_outcome_message("error",outcome["output"],the_type=outcome["the_type"])
        
        return generate_outcome_message("success","data logged in notion....")

    # What if during the process, something went wrong? Store it in notion. 
    def store_log_in_database(self,log_data):
            # CHECK LOG DATA TO SEE IF IT IS READY FOR STORAGE
            if isinstance(log_data,str) == False:
                return generate_outcome_message("error",{"status": False,"message": f"log_data parameter is not of type string..."},the_type="custom")
            splitted = log_data.split(",")
            table_column_number = len(self.logging_table_columns)
            data_length = len(splitted)
            # Check if the column length (exclude id and timestamp) is the same as the number of data specified
            if table_column_number != data_length:
                return generate_outcome_message("error",{"status": False,"message": f"Column number {table_column_number} is not the same as data length {data_length}..."},the_type="custom")

            # CHECK IF DATABASE IS REACHABLE
            if self.client == None:
                return generate_outcome_message("error",{"status": True, "message": f"client is empty..."},the_type="custom")
            if self.logging_table_name == None:
                return generate_outcome_message("error",{"status": True, "message": f"logging table name not specified..."},the_type="custom")
            if self.logging_table_columns == None:
                return generate_outcome_message("error",{"status" : True, "message": f"logging table columns for {self.logging_table_name} not specified..."},the_type="custom")
            
            # Construct the column name portion of the insert command (ADD timestamp column)
            stringing_columns = 'timestamp,'+",".join(self.logging_table_columns)
            
            # Get current date time (seconds precision)
            current_date_time = datetime.now()
            formatted_time = current_date_time.strftime('%Y-%m-%d %H:%M:%S')
            formatted_time = datetime.strptime(formatted_time, '%Y-%m-%d %H:%M:%S')
            timestamper = formatted_time.timestamp()
            
            string_format = f"TO_TIMESTAMP({timestamper}),"
            for index,i in enumerate(splitted):
                string_format += f"'{i}'"
                if index != data_length - 1:
                    string_format += "," 
            
            command = f"insert into {self.logging_table_name} ({stringing_columns}) values ({string_format})"
            
            try:
                outcome = self.client.execute(command)
                self.connection.commit()
            except psycopg2.Error as e:
                return generate_outcome_message("error",{"status": True,"message": f"Something went wrong with execution..."},the_type="others")
            
            return generate_outcome_message("success","data logged...")
        # if self.storage_location == "notion":



# # Local testing
# a = custom_logger()
# a.initialise_database("logging_data","usage_data")
# a.change_storage_location()
# def test():
#     print("lel:",a.store_log())
#     print("hello there.......")
# test()
