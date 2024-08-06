"""A class for securely storing and retrieving environment variables"""
from cryptography.fernet import Fernet
import os

class SecureEnv:
    def __init__(self, key):
        self.cipher = Fernet(key)

    def decrypt(self, value):
        if self.check_env_exists(value):
            return self.cipher.decrypt(os.environ[value]).decode()
        else:
            print("Environment variable not found.")
            choice = input("Would you like to enter the value for the environment variable "+value+" now? (y/n): ")
            if choice.lower() == "y":
                value = input("Enter the value for the environment variable "+value+": ")
                self.add_env(value, self.cipher.encrypt(value.encode()))
                return value
            else:
                print("Cannot continue without the environment variable.")
                print("Exiting program.")
                exit()
    
    def encrypt(self, value):
        return self.cipher.encrypt(value.encode())

    def check_env_exists(self, env_name):
        return env_name in os.environ
    
    def add_env(self, env_name, value):
        os.environ[env_name] = self.encrypt(value)