import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 읽어오기

BASE_DIR = os.path.dirname(__file__)

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
else:
    # .env 없을 때(팀원이 아직 세팅 전이거나) 로컬 SQLite로 폴백
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'par3.db'))

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'par3#project')