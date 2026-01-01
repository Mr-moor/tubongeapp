import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URI')
JWT_SECRET = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRE_DAYS = int(os.getenv('JWT_EXPIRE_DAYS', '7'))
S3_BUCKET = os.getenv('S3_BUCKET')
S3_REGION = os.getenv('S3_REGION', 'us-east-1')
S3_ENDPOINT = os.getenv('S3_ENDPOINT_URL') or None
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
RED_FLAG_THRESHOLD = int(os.getenv('RED_FLAG_THRESHOLD', '3'))

CELERY_BROKER = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1')
CELERY_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
