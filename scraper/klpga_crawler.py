import requests
from bs4 import BeautifulSoup
import json

url = "https://klpga.co.kr/load/record/loadPublicRecord"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://klpga.co.kr/web/record/publicRecordDetail",
    "X-Requested-With": "XMLHttpRequest"
}

response = requests.post(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select('table tr')
    
    players_list = []
    
    # 반복문을 돌며 각 행의 데이터 추출
    for row in rows:
        cols = row.find_all('td')
        
        # 칸이 3개 이상 있는 유효한 데이터 행일 때만 실행
        if len(cols) >= 3:
            # 1번째 칸 (인덱스 1): 순위
            rank = cols[1].text.strip()
            
            # 2번째 칸 (인덱스 2): 선수 이름
            name = cols[2].text.strip()
            
            # 3번째 칸 (인덱스 3): 상금
            prize = cols[3].text.strip()
            
            # 내가 알아보기 쉬운 이름표(Key)로 딕셔너리 만들기
            player_info = {
                "rank": rank,
                "name": name,
                "prize": prize 
            }
            
            players_list.append(player_info)
            
    # 결과를 JSON 파일로 저장
    with open("klpga_top3_cols.json", "w", encoding="utf-8") as f:
        json.dump(players_list, f, ensure_ascii=False, indent=4)
        
    print(f"총 {len(players_list)}명의 데이터를 성공적으로 추출하여 저장했습니다!")
    
    # 상위 3명만 미리보기로 출력해보기
    print("\n--- 상위 3명 미리보기 ---")
    for p in players_list[:3]:
        print(p)

else:
    print(f"통신 실패: {response.status_code}")
