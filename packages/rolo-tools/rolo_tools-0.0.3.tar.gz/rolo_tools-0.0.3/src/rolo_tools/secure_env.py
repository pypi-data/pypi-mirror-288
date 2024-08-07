"""A class for securely storing and retrieving environment variables"""
from cryptography.fernet import Fernet
import os

class SecureEnv:
    def __init__(self, key):
        if self.cipher is None:
            if os.environ['secure_env'] == "raw":
                self.mode = "raw"
            else:
                print("No key provided. Cannot encrypt or decrypt values.")
                print("If you have added your environment variables without encryption, set the 'secure_env' environment variable to 'raw'.")
                choice = input("Would you like to run raw for this session? (y/n): ")
                if choice.lower() == "y":
                    self.mode = "raw"
                else:
                    print("Please check package documentation for instructions on how to setup environment variables.")
                    print("Exiting program.")
                    exit()
        else:
            self.cipher = Fernet(key)
            self.mode = "encrypted"

    def decrypt(self, env_variable):
        if self.mode == "encrypted":
            if self.check_env_exists(env_variable):
                return self.cipher.decrypt(os.environ[env_variable]).decode()
            else:
                self.env_is_missing(env_variable)
        else:
            return os.environ[env_variable]
    
    def encrypt(self, value):
        if self.mode == "encrypted":
            return self.cipher.encrypt(value.encode())
        else:
            print("Cannot encrypt value. No key provided. Keys are provided when initializing the SecureEnv class.")
            choice = input("Would you like to generate a key now? (y/n): ")
            if choice.lower() == "y":
                key = Fernet.generate_key()
                print("Key generated: "+key.decode())
                print("Please store this key in a secure location.")
                self.cipher = Fernet(key)
                self.mode = "encrypted"
                return self.cipher.encrypt(value.encode())
            else:
                print("Cannot continue without a key.")
                print("Exiting program.")
                exit()

    def check_env_exists(self, env_name):
        return env_name in os.environ

    @staticmethod
    def env_is_missing(env_name):
        """Prints an error message and exits the program if an environment variable is missing"""
        print(f"{env_name} not found in environment variables")
        print("Please add it to the environment variables and try again")
        exit()        