# ============================================
# tour_api.py
# 한국관광공사 TourAPI 연동 유틸
# 작성자: 오지 (feature/join-page)
#
# 담당 기능:
#   - region, keyword 둘 다 선택적으로 받아서 골프장 검색
#     · region만 있으면: 그 지역 전체 골프장 목록
#     · keyword만 있으면: 전국에서 이름으로 검색
#     · 둘 다 있으면: 그 지역 안에서 이름으로 필터링
#
# ⚠️ 참고: TourAPI가 KorService1 → KorService2로 개편됨에 따라
#   areaBasedList2, searchKeyword2 엔드포인트로 사용 중
# ⚠️ 골프장은 이름에 "골프"가 없는 경우(예: "○○CC", "○○GC")가 많아서
#   서비스분류코드(cat3 = A03020700, 레포츠>육상레포츠>골프)로 필터링함
# ============================================

import os
import requests

TOUR_API_URL = "https://apis.data.go.kr/B551011/KorService2/areaBasedList2"
TOUR_API_SEARCH_URL = "https://apis.data.go.kr/B551011/KorService2/searchKeyword2"
TOUR_API_KEY = os.environ.get('TOUR_API_KEY')

# TourAPI 서비스분류코드 - 레포츠 > 육상 레포츠 > 골프
GOLF_CAT3_CODE = "A03020700"

# 화면에서 선택하는 지역명 → TourAPI areaCode
REGION_TO_AREACODE = {
    '서울': '1',
    '인천': '2',
    '대전': '3',
    '대구': '4',
    '광주': '5',
    '부산': '6',
    '울산': '7',
    '세종': '8',
    '경기': '31',
    '강원도': '32',
    '충청북도': '33',
    '충청남도': '34',
    '경상북도': '35',
    '경상남도': '36',
    '전라북도': '37',
    '전라남도': '38',
    '제주도': '39',
}


def search_golf_courses(region=None, keyword=None):
    """
    region, keyword를 조합해서 골프장 검색.
    - region만: 그 지역 전체 조회
    - keyword만: 전국에서 이름으로 검색
    - 둘 다: 그 지역 조회 후 keyword로 한 번 더 필터링
    """
    if not region and not keyword:
        return []

    if region:
        results = _search_by_area(region)
        if keyword:
            results = [r for r in results if keyword in r['name']]
        return results
    else:
        return _search_by_keyword(keyword)


def _search_by_area(region):
    area_code = REGION_TO_AREACODE.get(region)
    if not area_code:
        return []

    params = {
        'serviceKey': TOUR_API_KEY,
        'MobileOS': 'ETC',
        'MobileApp': 'PAR3',
        'areaCode': area_code,
        'contentTypeId': 28,   # 레포츠 (골프장 포함)
        '_type': 'json',
        'numOfRows': 100,
        'pageNo': 1,
        'arrange': 'A',
    }
    return _request_and_parse(TOUR_API_URL, params, region)


def _search_by_keyword(keyword):
    params = {
        'serviceKey': TOUR_API_KEY,
        'MobileOS': 'ETC',
        'MobileApp': 'PAR3',
        'keyword': keyword,
        'contentTypeId': 28,
        '_type': 'json',
        'numOfRows': 20,
        'pageNo': 1,
    }
    return _request_and_parse(TOUR_API_SEARCH_URL, params, None)


def _request_and_parse(url, params, region_label):
    """
    TourAPI 응답을 요청하고, 골프장 이름/지역/이미지만 뽑아서 리스트로 반환.
    items가 빈 문자열로 오는 경우(검색 결과 0건)까지 방어 처리함.
    """
    try:
        response = requests.get(url, params=params, timeout=15)
        data = response.json()

        items_raw = data['response']['body']['items']

        # 결과가 없을 때 items가 dict가 아니라 빈 문자열("")로 오는 경우가 있어서 방어
        if isinstance(items_raw, dict):
            items = items_raw.get('item', [])
        else:
            items = []

        # 결과가 1건일 땐 dict, 여러 건일 땐 list로 옴 → 리스트로 통일
        if isinstance(items, dict):
            items = [items]

        # ⚠️ 진단용 - 여기에 추가!
        print("=== 전체 항목 개수 ===")
        print(len(items))
        print("=== 전체 항목 title / cat3 목록 ===")
        for item in items:
            print(item.get('title', ''), '|', item.get('cat3', ''))

        results = []
        for item in items:
            title = item.get('title', '')
            cat3 = item.get('cat3', '')

            # 이름에 "골프"가 있거나, 분류코드가 골프(A03020700)인 경우만 포함
            if '골프' not in title and cat3 != GOLF_CAT3_CODE:
                continue

            results.append({
                'name': title,
                'region': region_label or '기타',
                'image': item.get('firstimage') or '',
                'content_id': item.get('contentid'),
            })
        return results

    except Exception as e:
        print('TourAPI 호출 오류:', e)
        return []