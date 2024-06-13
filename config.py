import configparser
import os

# from dotenv import load_dotenv
#
# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)
#
# # Loading token from .env
# MAIN_BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")
# DB_NAME = os.getenv("DB_NAME")

def ctf_get():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    return config

config = ctf_get()


db = config["DB"]
bot = config["Bot"]

MAIN_BOT_TOKEN = bot["MAIN_BOT_TOKEN"]
DB_USER = db["DB_USER"]
DB_PASS = db["DB_PASS"]
DB_NAME = db["DB_NAME"]
