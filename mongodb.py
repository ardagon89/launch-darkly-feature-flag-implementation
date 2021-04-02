"""Main class for database operations"""


# import the MongoClient class
from pymongo import MongoClient


# global variables for MongoDB host (default port is 27017)
DOMAIN = 'mongodb'
PORT = '27017'
USERNAME = 'admin'
PASSWORD = 'password'
TIMEOUT = 3000    # 3 second timeout

class Db():
    """A class used to perform database operations in mongodb"""
    
    @classmethod
    def get_client(cls):
        """ Get the client connection to mongodb.
                
        Returns:
            The MongoClient object
            
        Raises:
            SystemExit: If the database connection fails.
        """
        
        # Use a try-except indentation to catch MongoClient() errors
        try:
            
            # Try to instantiate a client instance
            client = MongoClient(
                host = [ DOMAIN + ":" + PORT ],
                serverSelectionTimeoutMS = TIMEOUT, 
                username = USERNAME,
                password = PASSWORD,
            )

            return client

        except errors.ServerSelectionTimeoutError as err:
            
            # catch pymongo.errors.ServerSelectionTimeoutError
            raise SystemExit(e)
            
            
    @classmethod
    def get_collection(cls):
        """ Get the users collection
                
        Returns:
            the users collection
            
        Raises:
            SystemExit: If the database connection fails.
        """
        
        # try to instantiate a client instance
        client = Db.get_client()
        mydb = client["launchdarkly"]
        
        return mydb["users"]

    @classmethod
    def get_feature_collection(cls):
        """ Get the features collection
                
        Returns:
            the features collection
            
        Raises:
            SystemExit: If the database connection fails.
        """
        
        # try to instantiate a client instance
        client = Db.get_client()
        mydb = client["launchdarkly"]
        
        return mydb["features"]

    @classmethod
    def get_log_collection(cls):
        """ Get the log collection
                
        Returns:
            the log collection
            
        Raises:
            SystemExit: If the database connection fails.
        """
        
        # try to instantiate a client instance
        client = Db.get_client()
        mydb = client["launchdarkly"]
        
        return mydb["log"]
            
            
    def get_server_version(self):
        """ Get the server version of mongodb
        
        Returns:
            Mongodb server version in string format
            
        Raises:
            SystemExit: If the database connection fails.
        """
        
        # try to instantiate a client instance
        client = Db.get_client()

        # return the version of MongoDB server if connection successful
        return "server version: " + client.server_info()["version"]
    
    
    def get_databases(self):
        """ Get a list of databases
                
        Returns:
            A list of databases in string format
            
        Raises:
            SystemExit: If the database connection fails.
        """
        
        # try to instantiate a client instance
        client = Db.get_client()

        # get the database_names from the MongoClient()
        return "databases: " + client.list_database_names()
            
    
    def get_one_doc(self):
        """ Get a user document

        Returns:
            Any one document from the users collection
            
        Raises:
            SystemExit: If the database connection fails.
        """
        
        mycollection = Db.get_collection()
        
        return mycollection.find_one()
    
    
    def get_all_docs(self):
        """ Get all user documents
        
        Returns:
            All documents from the users collection in list format
            
        Raises:
            SystemExit: If the database connection fails.
        """
        
        mycollection = Db.get_collection()
        
        return [rec for rec in mycollection.find()]
    
    
    def find_users(self, email):
        """ Get users having the provided email id
        
        Parameters: 
            - email: string
                Email id of the user
                
        Returns:
            List of User objects if the email id exists else None
            
        Raises:
            SystemExit: If the database connection fails.
        """
        
        mycollection = Db.get_collection()
    
        query = { "email": email }
        result_list = mycollection.find(query)
        
        return result_list
    
    
    def save_user(self, user_dict):
        """ Save a user in the db.
        
        Parameters: 
            - user_dict: dictionary
                Details of the user in dict format
                
        Returns:
            The id of the inserted record if insert successful else None
            
        Raises:
            SystemExit: If the database connection fails.
        """
        
        mycollection = Db.get_collection()
        result = mycollection.insert_one(user_dict)
        
        return result.inserted_id
    
    
    def save_users(self, user_list):
        """Save a list of users in the db.
        
        Parameters: 
            - user_list: list
                List of dictionary representation of users
                
        Returns:
            The ids of the inserted records if insert successful else None
            
        Raises:
            SystemExit: If the database connection fails.
        """
        
        mycollection = Db.get_collection()
        result = mycollection.insert_many(user_list)
        
        return result.inserted_ids

    def upsert_feature(self, flag, value):
        """ Save a feature in the db.
        
        Parameters: 
            - flag: string
                name of the feature flag
            - value: string
                value of the feature parameter
                
        Returns:
            The id of the inserted record if insert successful else None
            
        Raises:
            SystemExit: If the database connection fails.
        """
        
        mycollection = Db.get_feature_collection()
        result = mycollection.update({ "feature": flag }, {"feature": flag, "value": value}, upsert= True, multi= False)
        
        return result
    
    def get_feature(self, flag):
        """ Get the feature value with the given flag
        
        Parameters: 
            - flag: string
                name of the feature flag
                
        Returns:
            The feature if the flag exists else None
            
        Raises:
            SystemExit: If the database connection fails.
        """
        
        mycollection = Db.get_feature_collection()
    
        query = { "feature": flag }
        result_list = mycollection.find(query)
        
        return result_list

    def insert_log(self, flag, value, time, exec_time):
        """Save log parameters in the db.
    
        Parameters: 
            - flag: string
                Name of the feature
            - value: string
                Value of the feature
            - time: time
                Time of page load
            - exec_time: duration
                Page load duration
                
        Raises:
            SystemExit: If the database call fails.
        """
        
        mycollection = Db.get_log_collection()
        result = mycollection.insert_one({"feature":flag, "value":value, "time":time, "exec_time":exec_time})
        
        return result

    def get_logs(self, flag):
        """Get a feature logs from the db.
    
        Parameters: 
            - flag: string
                Name of the feature
            - value: string
                Value of the feature

        Returns:
            The result in the list or None
            
        Raises:
            SystemExit: If the database call fails.
        """
        
        mycollection = Db.get_log_collection()
    
        query = { "feature": flag }
        result_list = mycollection.find(query)
        
        return result_list