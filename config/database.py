import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
url = os.getenv('DATABASE_URL')
connection = psycopg2.connect(url)