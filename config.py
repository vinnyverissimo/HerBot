import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
PDF_DIR = 'files/'
