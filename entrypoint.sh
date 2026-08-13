#!/bin/sh
set -e

# 컨테이너 기동 시 DB 마이그레이션을 최신 상태로 적용한 뒤 앱을 실행
flask db upgrade

exec python app.py