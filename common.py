from dotenv import load_dotenv
from setup import ENV, TOKEN, IP, DIR_PATH, FILE_PATH
import os

if ENV:
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    IP = os.getenv("IP")
    DIR_PATH = os.getenv(r'DIR_PATH')
    FILE_PATH = os.getenv('FILE_PATH')

else:
    TOKEN = TOKEN
    IP = IP
    DIR_PATH = DIR_PATH
    FILE_PATH = FILE_PATH
