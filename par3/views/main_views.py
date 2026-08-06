import json
from flask import Blueprint, render_template, redirect, url_for
import os

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('intro.html')

@bp.route('/par3/')
def inter_par3():
    # --- 상금순위 Top 3 데이터 읽어오기 추가 ---
    json_path = "scraper/klpga_top3_cols.json"
    prize_top3_players = []
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            prize_top3_players = data[:3]  # 상위 3명만

    # --- 드라이버 비거리 Top 3 데이터 읽어오기 추가 ---
    json_path = "scraper/kpga_top10_drive.json"
    kpga_top3 = []
    #  파일이 존재하면 읽어와서 상위 3명만 쏙 뽑기
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 파이썬 리스트 슬라이싱으로 상위 3명만 자르기
            kpga_top3 = data[:3]

    return render_template('main.html',
                           prize_top3=prize_top3_players,
                           kpga_top3=kpga_top3)