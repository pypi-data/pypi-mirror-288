"""A simple logger class for logging to the console and a file."""
from datetime import datetime
import os, json

class Logger:
    def __init__(self, appname, source="General"):
        self.source = source #which part of the app is logging
        self.appname = appname #name of the app
    
    #Logging functions
    def commit(self, message):
        """Logs a string to the console and a file."""
        log_text = message + "\n"
        print(log_text)    
        self.write_to_file(log_text)

    def datetime(self, message):
        """Logs a string with a timestamp to the console and a file."""
        log_text = str(datetime.now())+" - " + message +"\n"
        print(log_text)
        self.write_to_file(log_text)       

    #JSON functions
    def json(self, json_obj):
        """Logs a JSON object to the console and a file."""
        log_text = json.dumps(json_obj, indent=4)
        print(log_text)
        self.write_to_file(log_text)

    def save_json_to_own_file(self, json_obj, filename):
        """Saves a JSON object to a file. Overwrites the file if it exists."""
        self.pretty_print_json(json_obj)
        with open(filename, 'w') as outfile:
            json.dump(json_obj, outfile, indent=4)        

    def pretty_print_json(self, json_obj): #only prints to console
        """Prints a JSON object to the console with indentation."""
        print(json.dumps(json_obj, indent=4))

    #File and directory functions
    def write_to_file(self, message):
        """Writes a string to a file."""
        log_path = "c:\\windows\\temp\\"+self.appname+"\\"+self.source+".log"
        log_parent_path = "c:\\windows\\temp\\"+self.appname+"\\"
        if not self.check_file_exists(log_path):
            if not self.check_directory_exists(log_parent_path):
                self.create_directory(log_parent_path)
            self.create_file(log_path)
        log_file = open(log_path, "a")
        log_file.write(message)
        log_file.close()     

    def check_file_exists(self, path):
        """Checks if a file exists."""
        try:
            open(path, 'r')
            return True
        except:
            return False
        
    def check_directory_exists(self, path):
        """Checks if a directory exists."""
        try:
            os.listdir(path)
            return True
        except:
            return False    

    def create_directory(self, path):
        """Creates a directory."""
        try:
            os.mkdir(path)
            return True
        except:
            return False

    def create_file(self, path):
        """Creates a file."""
        try:
            open(path, 'w')
            return True
        except:
            return False