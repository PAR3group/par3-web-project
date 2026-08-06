import re
from datetime import datetime
from par3 import create_app, db          # [수정] 실제 프로젝트의 app factory 경로에 맞게 조정
from par3.models import ShopProduct, ProductReview  # [수정] 실제 models.py 경로에 맞게 조정

products_data = [
    {
        "brand": "PXG", "title": "PXG CLUB 젠8 0311T 아이언", "rating": "4.7", "reviewCount": 89,
        "price": 2574000, "mainImg": "driver2.png", "detailImg": "detail2.jpg",
        "features": ["폭발적인 에너지를 공에 전달, 부드러운 타구감", "안정적인 샷과 정교한 구질 컨트롤", "PXG 코리아 정품 보증서 발송"],
        "reviews": ["디자인이 제 취향입니다.", "배송이 하루만에 왔어용"],
        "shipping": "무료배송", "origin": "Made in USA"
    },
    {
        "brand": "PXG", "title": "PXG 라이트닝 드라이버", "rating": "★★★★★ 4.9", "reviewCount": 152,
        "price": 990000, "mainImg": "driver.png", "detailImg": "detail.jpg",
        "features": ["압도적인 비거리 향상 기술력", "경량 카본 헤드 적용으로 스윙 스피드 극대화", "PXG 코리아 정품 보증서 발송"],
        "reviews": ["비거리 정말 잘 나가고 타구감도 좋습니다!", "배송도 빠르고 정품이라 만족함"],
        "shipping": "무료배송", "origin": "Made in USA"
    },
    {
        "brand": "PXG", "title": "PXG 젠7 0311P 블랙 아이언", "rating": "4.5", "reviewCount": 35,
        "price": 2496000, "mainImg": "driver3.png", "detailImg": "detail3.jpg",
        "features": ["AI 기술 기반 스마트 립 페이스 적용", "안정적인 라이각 및 일관된 롤링", "공식 대리점 정품"],
        "reviews": ["직진성이 매우 뛰어납니다.", "그립감이 쫀득해서 좋네요."],
        "shipping": "3,000원", "origin": "Made in USA"
    },
    {
        "brand": "PXG", "title": "PXG 젠6 0311P 아이언", "rating": "4.5", "reviewCount": 35,
        "price": 1980000, "mainImg": "driver4.png", "detailImg": "detail4.jpg",
        "features": ["AI 기술 기반 스마트 립 페이스 적용", "안정적인 라이각 및 일관된 롤링", "공식 대리점 정품"],
        "reviews": ["직진성이 매우 뛰어납니다.", "그립감이 쫀득해서 좋네요."],
        "shipping": "3,000원", "origin": "일본"
    },
    {
        "brand": "PXG", "title": "PXG 젠7 0311P 크롬 아이언 GEN7", "rating": "4.5", "reviewCount": 35,
        "price": 2376000, "mainImg": "driver5.png", "detailImg": "detail5.jpg",
        "features": ["AI 기술 기반 스마트 립 페이스 적용", "안정적인 라이각 및 일관된 롤링", "공식 대리점 정품"],
        "reviews": ["직진성이 매우 뛰어납니다.", "그립감이 쫀득해서 좋네요."],
        "shipping": "3,000원", "origin": "일본"
    },
    {
        "brand": "PING", "title": "PING G440 K HL DRIVER", "rating": "4.5", "reviewCount": 35,
        "price": 1060000, "mainImg": "driver6.png", "detailImg": "detail6.jpg",
        "features": ["AI 기술 기반 스마트 립 페이스 적용", "안정적인 라이각 및 일관된 롤링", "공식 대리점 정품"],
        "reviews": ["직진성이 매우 뛰어납니다.", "그립감이 쫀득해서 좋네요."],
        "shipping": "3,000원", "origin": "일본"
    },
    {
        "brand": "PING", "title": "PING G440 IRON", "rating": "4.5", "reviewCount": 35,
        "price": 2150000, "mainImg": "driver7.png", "detailImg": "detail7.jpg",
        "features": ["AI 기술 기반 스마트 립 페이스 적용", "안정적인 라이각 및 일관된 롤링", "공식 대리점 정품"],
        "reviews": ["직진성이 매우 뛰어납니다.", "그립감이 쫀득해서 좋네요."],
        "shipping": "3,000원", "origin": "일본"
    },
    {
        "brand": "PING", "title": "GLE4 IRON SET", "rating": "4.5", "reviewCount": 35,
        "price": 2170000, "mainImg": "driver8.png", "detailImg": "detail8.jpg",
        "features": ["AI 기술 기반 스마트 립 페이스 적용", "안정적인 라이각 및 일관된 롤링", "공식 대리점 정품"],
        "reviews": ["직진성이 매우 뛰어납니다.", "그립감이 쫀득해서 좋네요."],
        "shipping": "3,000원", "origin": "일본"
    },
    {
        "brand": "PING", "title": "BLUEPRINT T IRON", "rating": "4.5", "reviewCount": 35,
        "price": 2130000, "mainImg": "driver9.png", "detailImg": "detail9.jpg",
        "features": ["AI 기술 기반 스마트 립 페이스 적용", "안정적인 라이각 및 일관된 롤링", "공식 대리점 정품"],
        "reviews": ["직진성이 매우 뛰어납니다.", "그립감이 쫀득해서 좋네요."],
        "shipping": "3,000원", "origin": "일본"
    },
    {
        "brand": "PING", "title": "i540 IRON", "rating": "4.5", "reviewCount": 35,
        "price": 2280000, "mainImg": "driver10.png", "detailImg": "detail10.jpg",
        "features": ["AI 기술 기반 스마트 립 페이스 적용", "안정적인 라이각 및 일관된 롤링", "공식 대리점 정품"],
        "reviews": ["직진성이 매우 뛰어납니다.", "그립감이 쫀득해서 좋네요."],
        "shipping": "3,000원", "origin": "일본"
    },
    {
        "brand": "Callaway", "title": "가을 남성 시그니처 로고 티셔츠", "rating": "4.5", "reviewCount": 35,
        "price": 138000, "mainImg": "driver11.png", "detailImg": "detail11.jpg",
        "features": ["AI 기술 기반 스마트 립 페이스 적용", "안정적인 라이각 및 일관된 롤링", "공식 대리점 정품"],
        "reviews": ["직진성이 매우 뛰어납니다.", "그립감이 쫀득해서 좋네요."],
        "shipping": "3,000원", "origin": "일본"
    },
    {
        "brand": "Callaway", "title": "여름 여성 홑겹 블루종", "rating": "4.5", "reviewCount": 35,
        "price": 398000, "mainImg": "driver12.png", "detailImg": "detail12.jpg",
        "features": ["AI 기술 기반 스마트 립 페이스 적용", "안정적인 라이각 및 일관된 롤링", "공식 대리점 정품"],
        "reviews": ["직진성이 매우 뛰어납니다.", "그립감이 쫀득해서 좋네요."],
        "shipping": "3,000원", "origin": "일본"
    },
    {
        # [참고] 이 상품만 detailImg가 아니라 detailImgs(배열)로 되어 있어서, 첫 번째 이미지만 detail_img에 저장됨
        "brand": "Callaway", "title": "[온라인 단독] 크롬투어 트루비스 핫도그 에디션 (공식몰 리미티드)",
        "rating": "★★★★★ 5.0", "reviewCount": 204, "price": 75900,
        "mainImg": "driver13.png", "detailImgs": ["detail13.jpg", "detail13-2.jpg"],
        "features": ["정밀하게 설계된 투어 우레탄 커버", "온라인 단독"],
        "reviews": ["디자인이 댕귀야움.", "잘 산거 같아여"],
        "shipping": "우체국 택배 / 30만원 이상 결제시 무료배송", "origin": "Made in USA"
    },
    {
        "brand": "Callaway", "title": "[온라인 단독] 오퍼스 플래티넘 크래프츠맨 컬렉션 웨지: 해머드 카퍼 (공식몰 리미티드)",
        "rating": "4.5", "reviewCount": 35, "price": 352000,
        "mainImg": "driver14.png", "detailImg": "detail14.jpg",
        "features": ["AI 기술 기반 스마트 립 페이스 적용", "안정적인 라이각 및 일관된 롤링", "공식 대리점 정품"],
        "reviews": ["직진성이 매우 뛰어납니다.", "그립감이 쫀득해서 좋네요."],
        "shipping": "3,000원", "origin": "일본"
    },
    {
        "brand": "Callaway", "title": "C-SPROT 스탠드백", "rating": "4.5", "reviewCount": 35,
        "price": 350000, "mainImg": "driver15.png", "detailImg": "detail15.jpg",
        "features": ["AI 기술 기반 스마트 립 페이스 적용", "안정적인 라이각 및 일관된 롤링", "공식 대리점 정품"],
        "reviews": ["직진성이 매우 뛰어납니다.", "그립감이 쫀득해서 좋네요."],
        "shipping": "3,000원", "origin": "일본"
    },
    {
        "brand": "TAYLORMADE", "title": "2026 ★특가★ TP5 하프더즌 골프공", "rating": "4.5", "reviewCount": 35,
        "price": 46000, "mainImg": "driver16.png", "detailImg": "detail16.jpg",
        "features": ["AI 기술 기반 스마트 립 페이스 적용", "안정적인 라이각 및 일관된 롤링", "공식 대리점 정품"],
        "reviews": ["직진성이 매우 뛰어납니다.", "그립감이 쫀득해서 좋네요."],
        "shipping": "3,000원", "origin": "일본"
    },
    {
        "brand": "TAYLORMADE", "title": "26SS 남성 스트레치 버킷햇 T8031H61628-509", "rating": "4.5", "reviewCount": 35,
        "price": 118000, "mainImg": "driver17.png", "detailImg": "detail17.jpg",
        "features": ["AI 기술 기반 스마트 립 페이스 적용", "안정적인 라이각 및 일관된 롤링", "공식 대리점 정품"],
        "reviews": ["직진성이 매우 뛰어납니다.", "그립감이 쫀득해서 좋네요."],
        "shipping": "3,000원", "origin": "일본"
    },
    {
        "brand": "TAYLORMADE", "title": "K-컬렉션 골프 카트백 캐디백 TL885", "rating": "4.5", "reviewCount": 35,
        "price": 490000, "mainImg": "driver18.png", "detailImg": "detail18.jpg",
        "features": ["AI 기술 기반 스마트 립 페이스 적용", "안정적인 라이각 및 일관된 롤링", "공식 대리점 정품"],
        "reviews": ["직진성이 매우 뛰어납니다.", "그립감이 쫀득해서 좋네요."],
        "shipping": "3,000원", "origin": "일본"
    },
    {
        "brand": "TAYLORMADE", "title": "26SS 여성 리본 잔플리츠 큐롯 T8031C66491-100", "rating": "4.5", "reviewCount": 35,
        "price": 258000, "mainImg": "driver19.png", "detailImg": "detail19.jpg",
        "features": ["AI 기술 기반 스마트 립 페이스 적용", "안정적인 라이각 및 일관된 롤링", "공식 대리점 정품"],
        "reviews": ["직진성이 매우 뛰어납니다.", "그립감이 쫀득해서 좋네요."],
        "shipping": "3,000원", "origin": "일본"
    },
]


def parse_rating(raw_rating):
    """[추가] '★★★★★ 4.9' 처럼 별표가 섞인 문자열에서도 숫자만 뽑아서 float으로 변환"""
    match = re.search(r'\d+(\.\d+)?', str(raw_rating))
    return float(match.group()) if match else 0.0


def seed_products(data):
    for item in data:
        existing = ShopProduct.query.filter_by(
            brand=item["brand"], title=item["title"]
        ).first()

        if existing:
            print(f"이미 존재함, 건너뜀: {item['brand']} - {item['title']}")
            continue

        # [수정] detailImg 또는 detailImgs(배열) 둘 다 처리 - 배열이면 첫 번째 이미지만 사용
        if "detailImgs" in item and item["detailImgs"]:
            detail_img = item["detailImgs"][0]
        else:
            detail_img = item.get("detailImg")

        new_product = ShopProduct(
            brand=item["brand"],
            title=item["title"],
            rating=parse_rating(item["rating"]),
            review_count=item.get("reviewCount", 0),
            price=item["price"],
            main_img=item.get("mainImg", "no_image.png"),
            detail_img=detail_img,
            features=item.get("features", []),
            shipping=item.get("shipping"),
            origin=item.get("origin"),
        )
        db.session.add(new_product)
        db.session.flush()

        for review_text in item.get("reviews", []):
            new_review = ProductReview(
                product_id=new_product.id,
                content=review_text,
                created_at=datetime.now()
            )
            db.session.add(new_review)

        print(f"등록 완료: {item['brand']} - {item['title']}")

    db.session.commit()
    print(f"전체 {len(data)}개 시드 데이터 처리 완료!")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_products(products_data)