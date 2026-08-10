import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 읽어오기

BASE_DIR = os.path.dirname(__file__)

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    # Supabase 세션 풀러(port 5432)는 프로젝트 전체 동시 연결이 15개로 제한됨.
    # 기본값(pool_size 5 + max_overflow 10 = 15)을 쓰면 로컬 프로세스 하나가
    # 전체 한도를 다 써버릴 수 있어 팀원 수만큼 여유가 남도록 낮춰둠.
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 3,
        'max_overflow': 2,
        'pool_recycle': 280,
        'pool_pre_ping': True,
    }
else:
    # .env 없을 때(팀원이 아직 세팅 전이거나) 로컬 SQLite로 폴백
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'par3.db'))

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'par3#project')
# Supabase Storage (이미지 업로드)
SUPABASE_URL = os.environ.get('SUPABASE_URL', '').rstrip('/')
SUPABASE_SERVICE_ROLE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
SUPABASE_STORAGE_BUCKET = os.environ.get('SUPABASE_STORAGE_BUCKET', 'images')