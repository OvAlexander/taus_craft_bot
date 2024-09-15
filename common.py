from dotenv import load_dotenv
from setup import ENV, TOKEN, IP, SERVER_DIR_PATH, FILE_PATH
import os

DIR_PATH = os.getcwd()
if ENV:
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    IP = os.getenv("IP")
    SERVER_DIR_PATH = os.getenv(r'SERVER_DIR_PATH')
    FILE_PATH = os.getenv('FILE_PATH')
    CHANNEL_ID = os.getenv('CHANNEL_ID')
    NOTI_LIST = os.getenv('NOTI_LIST')

else:
    TOKEN = TOKEN
    IP = IP
    SERVER_DIR_PATH = SERVER_DIR_PATH
    FILE_PATH = FILE_PATH
