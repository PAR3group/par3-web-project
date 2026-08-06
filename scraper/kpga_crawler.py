import requests
import json

url = "https://api.kpga.co.kr/record/detail"

params = {
    "tourId": "11",
    "year": "2026",
    "menuId": "9",
    "playerType": ""
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.kpga.co.kr/"
}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    raw_data = response.json()

    # 보내주신 구조를 보면 최상위 딕셔너리 안에 "records"라는 키로 리스트가 들어있습니다.
    record_list = raw_data.get("records", [])

    player_list = []

    # 상위 10명만 자르기 (slice [:10])
    for item in record_list[:10]:
        # 정확히 일치하는 키 이름 매핑
        rank = item.get("ranking", "")       # 순위
        name = item.get("playerName", "")   # 선수이름
        record_raw = item.get("record", "") # 평균 드라이브 거리(기록)

        # 소수점 두 자리까지만 남기기
        try:
            record = round(float(record_raw), 2)
        except (TypeError, ValueError):
            record = record_raw  # 숫자로 변환 안 되면 원본 그대로 둠

        parsed_item = {
            "rank": rank,
            "name": name,
            "record": record
        }
        player_list.append(parsed_item)

    # JSON 파일로 저장하기
    with open("kpga_top10_drive.json", "w", encoding="utf-8") as f:
        json.dump(player_list, f, ensure_ascii=False, indent=4)

    print("평균 드라이브 거리 상위 10명 추출 완료!")
    for p in player_list:
        print(f"{p['rank']}위 | {p['name']} | {p['record']}야드")

else:
    print(f"통신 실패: {response.status_code}")