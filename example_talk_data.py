from datetime import datetime

# 사용 가능한 이미지 리스트 (요청하신 파일명 반영)
# [수정] url_for('static', filename=...) 이 실제로 만드는 형식과 동일하게
#        앞에 '/'를 붙여서 저장 (라우트 함수 저장 형식과 일치)
images = [
    "/static/img/banner_main.png",
    "/static/img/namseoul.png",
    "/static/img/rec_D.png",
    "/static/img/midus.png",
    "/static/img/rec_I.png",
    "/static/img/rec_U.png",
    "/static/img/rec_W.png"
]

# 30개의 골프 커뮤니티 예시 게시글
sample_posts_data = [
    {
        "category": "라운드후기",
        "title": "오늘 남서울CC 다녀왔는데 그린피 아깝지 않네요",
        "content": "페어웨이 컨디션도 최상이고 날씨도 완벽했습니다. 다만 전반에 퍼팅이 다 무너져서 아쉽네요ㅜㅜ",
        "author": "싱글을꿈꾸며",
        "image_url": "/static/img/namseoul.png",
        "is_video": False,
        "views": 245,
        "likes": 32
    },
    {
        "category": "스윙고민",
        "title": "드라이버만 잡으면 슬라이스 나시는 분들 필독",
        "content": "아웃사이더 궤도 고치려고 아예 등 뒤로 엎어 친다는 느낌으로 치니까 죽던 볼이 살기 시작했습니다. 조언 좀 부탁드려요.",
        "author": "백돌이탈출러",
        "image_url": "/static/img/rec_D.png",
        "is_video": False,
        "views": 412,
        "likes": 58
    },
    {
        "category": "장비질문",
        "title": "아이언 샤프트 NS PRO 950 vs 다이나믹골드 S200",
        "content": "지금 950 쓰는데 약간 날리는 느낌이 있어서 S200으로 가볼까 고민 중입니다. 체력 부담이 많이 될까요?",
        "author": "골프치는곰",
        "image_url": "/static/img/midus.png",
        "is_video": False,
        "views": 180,
        "likes": 14
    },
    {
        "category": "자유",
        "title": "스크린 골프 18홀 돌고 나면 손바닥 아픈 거 저만 그런가요?",
        "content": "매트가 딱딱해서 그런지 스윙 몇 번 시게 하면 손에 물집 잡히거나 찌릿하네요. 장갑 좋은 거 추천 좀...",
        "author": "스크린광인",
        "image_url": "/static/img/rec_I.png",
        "is_video": False,
        "views": 150,
        "likes": 19
    },
    {
        "category": "정보",
        "title": "[꿀팁] 필드 나가기 전 꼭 체크해야 할 골프룰 변경점",
        "content": "올해부터 바뀐 로컬룰이나 페널티 구역 처리 방법 간단하게 요약해 봤습니다. 동반자한테 아는 척하기 딱 좋습니다.",
        "author": "룰마스터",
        "image_url": "/static/img/banner_main.png",
        "is_video": False,
        "views": 320,
        "likes": 45
    },
    {
        "category": "유머",
        "title": "골프 치는 사람들이 가장 많이 하는 거짓말 TOP 3",
        "content": "1위: '나 오늘 그립 잡는 법 바꿨어'\n2위: '이번 홀만 끝나면 골프 때려치운다'\n3위: '나 골프 안 친 지 오래됐다'\n공감하시나요? ㅋㅋ",
        "author": "보기플레이어",
        "image_url": "/static/img/rec_U.png",
        "is_video": False,
        "views": 580,
        "likes": 92
    },
    {
        "category": "라운드후기",
        "title": "제주도 명문 골프장 다녀온 후기 (사진 많음)",
        "content": "바다 보면서 티샷 날리니까 속이 다 뻥 뚫리네요. 그린피는 사악하지만 일 년에 한 번쯤은 올 만합니다.",
        "author": "제주도민골퍼",
        "image_url": "/static/img/rec_W.png",
        "is_video": False,
        "views": 310,
        "likes": 41
    },
    {
        "category": "스윙고민",
        "title": "아이언 뒷땅 치는 버릇 어떻게 고치나요?",
        "content": "공만 맞추려고 하면 몸이 일어서거나 임팩트 때 손목이 풀려버립니다. 레슨을 받아도 그때뿐이네요.",
        "author": "뒷땅제조기",
        "image_url": "/static/img/namseoul.png",
        "is_video": False,
        "views": 210,
        "likes": 22
    },
    {
        "category": "장비질문",
        "title": "퍼터 추천 부탁드립니다. 말렛 vs 블레이드",
        "content": "직진성이 좋다는 말렛으로 넘어가려고 하는데 거리감 맞추기 어렵다는 소리가 있어서 망설여지네요.",
        "author": "퍼팅지옥",
        "image_url": "/static/img/rec_D.png",
        "is_video": False,
        "views": 195,
        "likes": 15
    },
    {
        "category": "자유",
        "title": "주말 골프 라운드 취소됐습니다... 비 참 밉네요",
        "content": "한 달 전부터 잡은 부부 동반 라운딩인데 비 예보 때문에 결국 취소했습니다. 오늘 하루 종일 우울할 예정입니다.",
        "author": "비오는날",
        "image_url": "/static/img/midus.png",
        "is_video": False,
        "views": 135,
        "likes": 8
    },
    {
        "category": "정보",
        "title": "골프공 브랜드별 타구감과 스핀량 총정리",
        "content": "프로v1부터 타이틀리스트, 스릭슨, 볼빅까지 주요 3피스/4피스 볼 비교해 드립니다.",
        "author": "볼덕후",
        "image_url": "/static/img/rec_I.png",
        "is_video": False,
        "views": 390,
        "likes": 50
    },
    {
        "category": "유머",
        "title": "해저드에 볼 10개 빠트리고 깨달은 점",
        "content": "로스트볼은 죄가 없습니다. 죄는 제 스윙과 로또 같은 방향성에 있죠... 오늘 로스트볼 세트 또 주문했습니다.",
        "author": "볼줍는사람",
        "image_url": "/static/img/rec_U.png",
        "is_video": False,
        "views": 460,
        "likes": 74
    },
    {
        "category": "라운드후기",
        "title": "야간 라운드 처음 가봤는데 생각보다 괜찮네요",
        "content": "공 찾는 게 조금 힘들긴 한데 조명이 밝아서 라이트 체감도 좋고 직장인들한테는 최고인 듯합니다.",
        "author": "야간조명러버",
        "image_url": "/static/img/banner_main.png",
        "is_video": False,
        "views": 220,
        "likes": 27
    },
    {
        "category": "스윙고민",
        "title": "드라이버 비거리 200m 벽에 부딪혔습니다",
        "content": "볼스피드는 60 후반 나오는데 여기서 더 안 늘어나네요. 하체 회전 타이밍이 문제일까요?",
        "author": "장타꿈나무",
        "image_url": "/static/img/rec_W.png",
        "is_video": False,
        "views": 280,
        "likes": 33
    },
    {
        "category": "장비질문",
        "title": "골프 거리측정기 가성비 제품 추천해 주세요",
        "content": "부쉬넬은 너무 비싸고 20~30만 원대 중에서 핀처지 빠르고 오차 없는 모델 찾고 있습니다.",
        "author": "시력보정",
        "image_url": "/static/img/namseoul.png",
        "is_video": False,
        "views": 260,
        "likes": 20
    },
    {
        "category": "자유",
        "title": "드디어 오늘 첫 싱글 달성했습니다!!",
        "content": "골프 입문한 지 3년 만에 드디어 79타 쳤네요! 너무 기뻐서 주저리주저리 남겨봅니다. 다들 나이스샷 하세요!",
        "author": "싱글달성자",
        "image_url": "/static/img/rec_D.png",
        "is_video": False,
        "views": 620,
        "likes": 120
    },
    {
        "category": "정보",
        "title": "초보 골퍼를 위한 골프웨어 매너 및 복장 가이드",
        "content": "카라티 필수인지, 반바지는 어디까지 허용되는지, 골프화는 꼭 스파이크여야 하는지 정리했습니다.",
        "author": "패션테리블",
        "image_url": "/static/img/midus.png",
        "is_video": False,
        "views": 340,
        "likes": 38
    },
    {
        "category": "유머",
        "title": "동반자가 '나 오늘 힘 빼고 친다'고 할 때의 위험성",
        "content": "그 말을 하는 순간 그 홀은 OB나 해저드로 직행합니다. 절대 믿으면 안 되는 마성의 대사죠.",
        "author": "프로속닥러",
        "image_url": "/static/img/rec_I.png",
        "is_video": False,
        "views": 490,
        "likes": 85
    },
    {
        "category": "라운드후기",
        "title": "명문 회원제 골프장 초청받아 다녀왔습니다",
        "content": "관리 상태가 진짜 대박이더군요. 잔디가 카펫 밟는 줄 알았습니다. 스코어는 망했지만 눈이 호강했네요.",
        "author": "초대받은남자",
        "image_url": "/static/img/rec_U.png",
        "is_video": False,
        "views": 270,
        "likes": 29
    },
    {
        "category": "스윙고민",
        "title": "어프로치 거리 조절 팁 전수해 주세요",
        "content": "30미치든 50미터든 맨날 그린 오버하거나 짧아서 3퍼트로 이어집니다. 시계추 스윙이 답인가요?",
        "author": "숏게임장애",
        "image_url": "/static/img/rec_W.png",
        "is_video": False,
        "views": 315,
        "likes": 44
    },
    {
        "category": "장비질문",
        "title": "골프백(캐디백) 스탠드백 vs 투어백 어떤 게 편한가요?",
        "content": "차가 작아서 실을 때 편한 거 찾고 있는데 스탠드백이 관리하기 편할지 궁금합니다.",
        "author": "짐보따리",
        "image_url": "/static/img/banner_main.png",
        "is_video": False,
        "views": 165,
        "likes": 11
    },
    {
        "category": "자유",
        "title": "스크린 골프 핸디캡 룰 질문 있습니다",
        "content": "친구들이랑 스크린 치는데 멀리건 개수랑 컨시드 거리를 다르게 해서 매번 싸우네요. 보통 다들 어떻게 타협하시나요?",
        "author": "내기골퍼",
        "image_url": "/static/img/namseoul.png",
        "is_video": False,
        "views": 205,
        "likes": 16
    },
    {
        "category": "정보",
        "title": "골프 연습장(인도어) 이용할 때 층수 고르는 팁",
        "content": "1층이 공 날아가는 거 보기 좋지만 바람이나 매트 상태 때문에 상층부가 나을 때도 있습니다. 주관적인 팁 공유해요.",
        "author": "연습벌레",
        "image_url": "/static/img/rec_D.png",
        "is_video": False,
        "views": 240,
        "likes": 25
    },
    {
        "category": "유머",
        "title": "캐디 분께 밉보이지 않는 초보의 처세술",
        "content": "공 안 찾아진다고 짜증 내지 않기, 멀리건 달라고 조르지 않기, 공 미리 세 개씩 들고 다니기 등등 웃프네요 ㅋㅋ",
        "author": "매너남",
        "image_url": "/static/img/midus.png",
        "is_video": False,
        "views": 530,
        "likes": 95
    },
    {
        "category": "라운드후기",
        "title": "지방 투어 골프 여행 1박 2일 다녀왔습니다",
        "content": "맛집도 가고 하루에 두 탕씩 돌았더니 몸은 녹아내리는데 골프 재미는 확실히 배가 되네요.",
        "author": "여행쟁이",
        "image_url": "/static/img/rec_I.png",
        "is_video": False,
        "views": 210,
        "likes": 24
    },
    {
        "category": "스윙고민",
        "title": "아이언 생크(shank) 나기 시작하면 어떻게 치료하나요?",
        "content": "넥 부분에 툭툭 맞으면서 오른쪽으로 꺾여 나가는데 원인을 모르겠습니다. 연습 중단하고 쉬어야 할까요?",
        "author": "생크공포증",
        "image_url": "/static/img/rec_U.png",
        "is_video": False,
        "views": 380,
        "likes": 52
    },
    {
        "category": "장비질문",
        "title": "골프화 스파이크리스 vs 소프트스파이크 추천",
        "content": "필드랑 스크린 겸용으로 신으려고 하는데 미끄러지지 않는 건 역시 스파이크가 낫겠죠?",
        "author": "발편한게최고",
        "image_url": "/static/img/rec_W.png",
        "is_video": False,
        "views": 185,
        "likes": 13
    },
    {
        # [수정] 영상 게시글: image_url을 static/video/intro.mp4 경로로, is_video=True 유지
        "category": "자유",
        "title": "골프 유튜브 채널 누구 보시나요?",
        "content": "요즘 김구라쇼나 심스윙, 에이지슈터 등등 보는데 도움 되는 채널 있으면 하나씩 추천해 주세요!",
        "author": "유튜브홀릭",
        "image_url": "/static/video/intro.mp4",
        "is_video": True,
        "views": 290,
        "likes": 30
    },
    {
        "category": "정보",
        "title": "캐디피 및 골프장 부대비용 인상 체감 후기",
        "content": "캐디피부터 그늘집 가격까지 점점 올라서 1인 라운딩 비용이 부담되는 시대네요. 정보 공유합니다.",
        "author": "경제적인골퍼",
        "image_url": "/static/img/namseoul.png",
        "is_video": False,
        "views": 310,
        "likes": 43
    },
    {
        "category": "유머",
        "title": "퍼팅 라인 읽을 때 캐디님 말과 내 생각을 일치시키는 법",
        "content": "캐디님은 '오른쪽 한 컵 반'이라는데 내 눈에는 '왼쪽 반 컵'으로 보여서 내 맘대로 쳤다가 3퍼트 한 썰.",
        "author": "똥고집",
        "image_url": "/static/img/rec_D.png",
        "is_video": False,
        "views": 440,
        "likes": 76
    }
]

def init_sample_posts():
    """example_talk_data의 30개 예시 글을 데이터베이스에 추가하는 함수"""
    # 순환 참조 방지를 위해 함수 내부에서 임포트
    from par3 import db, create_app         # 본인 플라스크 앱 파일명에 맞게 수정 (예: from main import db)
    from par3.models import Post     # 본인 모델 파일명에 맞게 수정
    app = create_app()
    with app.app_context():
        try:
            for data in sample_posts_data:
                post = Post(
                    category=data["category"],
                    title=data["title"],
                    content=data["content"],
                    author=data["author"],
                    image_url=data["image_url"],
                    is_video=data["is_video"],
                    views=data["views"],
                    likes=data["likes"]
                )
                db.session.add(post)

            db.session.commit()
            print("✅ 골프 예시 게시글 30개가 데이터베이스에 성공적으로 추가되었습니다!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ 데이터 추가 중 오류 발생: {e}")

# 스크립트 직접 실행 시 함수 호출
if __name__ == "__main__":
    init_sample_posts()