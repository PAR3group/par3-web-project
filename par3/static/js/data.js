// data.js
const products = [
  {
    id: 1, // URL의 ?id=1 과 연결됨
    brand: "PXG",
    title: "PXG CLUB 젠8 0311T 아이언",
    rating: "4.7",
    reviewCount: 89,
    price: 2574000,
    mainImg: "driver2.png",       // 1번 상품 대표 이미지
    detailImg: "detail2.jpg",     // 1번 상품 상세 페이지 이미지
    features: [
      "폭발적인 에너지를 공에 전달, 부드러운 타구감",
      "안정적인 샷과 정교한 구질 컨트롤",
      "PXG 코리아 정품 보증서 발송"
    ],
    reviews: [
      "디자인이 제 취향입니다.",
      "배송이 하루만에 왔어용"
    ],
    shipping: "무료배송",
    origin: "Made in USA"
  },
  {
    id: 2, // URL의 ?id=2 와 연결됨
    brand: "PXG",
    title: "PXG 라이트닝 드라이버",
    rating: "★★★★★ 4.9",
    reviewCount: 152,
    price: 990000,
    mainImg: "driver.png",     // 2번 상품 전용 이미지
    detailImg: "detail.jpg", // 2번 상품 전용 이미지
    features: [
      "압도적인 비거리 향상 기술력",
      "경량 카본 헤드 적용으로 스윙 스피드 극대화",
      "PXG 코리아 정품 보증서 발송"
    ],
    reviews: [
      "비거리 정말 잘 나가고 타구감도 좋습니다!",
      "배송도 빠르고 정품이라 만족함"
    ],
    shipping: "무료배송",
    origin: "Made in USA"
  },
  {
    id: 3, // URL의 ?id=3 과 연결됨
    brand: "PXG",
    title: "PXG 젠7 0311P 블랙 아이언",
    rating: "4.5",
    reviewCount: 35,
    price: 2496000,
    mainImg: "driver3.png",
    detailImg: "detail3.jpg",
    features: [
      "AI 기술 기반 스마트 립 페이스 적용",
      "안정적인 라이각 및 일관된 롤링",
      "공식 대리점 정품"
    ],
    reviews: [
      "직진성이 매우 뛰어납니다.",
      "그립감이 쫀득해서 좋네요."
    ],
    shipping: "3,000원",
    origin: "Made in USA"
  },
  {
    id: 4, // URL의 ?id=3 과 연결됨
    brand: "PXG",
    title: "PXG 젠6 0311P 아이언",
    rating: "4.5",
    reviewCount: 35,
    price: 1980000,
    mainImg: "driver4.png",
    detailImg: "detail4.jpg",
    features: [
      "AI 기술 기반 스마트 립 페이스 적용",
      "안정적인 라이각 및 일관된 롤링",
      "공식 대리점 정품"
    ],
    reviews: [
      "직진성이 매우 뛰어납니다.",
      "그립감이 쫀득해서 좋네요."
    ],
    shipping: "3,000원",
    origin: "일본"
  },
  {
    id: 5, // URL의 ?id=3 과 연결됨
    brand: "PXG",
    title: "PXG 젠7 0311P 크롬 아이언 GEN7",
    rating: "4.5",
    reviewCount: 35,
    price: 2376000,
    mainImg: "driver5.png",
    detailImg: "detail5.jpg",
    features: [
      "AI 기술 기반 스마트 립 페이스 적용",
      "안정적인 라이각 및 일관된 롤링",
      "공식 대리점 정품"
    ],
    reviews: [
      "직진성이 매우 뛰어납니다.",
      "그립감이 쫀득해서 좋네요."
    ],
    shipping: "3,000원",
    origin: "일본"
  },
  {
  id: 6, // URL의 ?id=3 과 연결됨
  brand: "PING",
  title: "PING G440 K HL DRIVER",
  rating: "4.5",
  reviewCount: 35,
  price: 1060000,
  mainImg: "driver6.png",
  detailImg: "detail6.jpg",
  features: [
    "AI 기술 기반 스마트 립 페이스 적용",
    "안정적인 라이각 및 일관된 롤링",
    "공식 대리점 정품"
  ],
  reviews: [
    "직진성이 매우 뛰어납니다.",
    "그립감이 쫀득해서 좋네요."
  ],
  shipping: "3,000원",
  origin: "일본"
  },
  {
  id: 7, // URL의 ?id=3 과 연결됨
  brand: "PING",
  title: "PING G440 IRON",
  rating: "4.5",
  reviewCount: 35,
  price: 2150000,
  mainImg: "driver7.png",
  detailImg: "detail7.jpg",
  features: [
    "AI 기술 기반 스마트 립 페이스 적용",
    "안정적인 라이각 및 일관된 롤링",
    "공식 대리점 정품"
  ],
  reviews: [
    "직진성이 매우 뛰어납니다.",
    "그립감이 쫀득해서 좋네요."
  ],
  shipping: "3,000원",
  origin: "일본"
  },
  {
  id: 8, // URL의 ?id=3 과 연결됨
  brand: "PING",
  title: "GLE4 IRON SET",
  rating: "4.5",
  reviewCount: 35,
  price: 2170000,
  mainImg: "driver8.png",
  detailImg: "detail8.jpg",
  features: [
    "AI 기술 기반 스마트 립 페이스 적용",
    "안정적인 라이각 및 일관된 롤링",
    "공식 대리점 정품"
  ],
  reviews: [
    "직진성이 매우 뛰어납니다.",
    "그립감이 쫀득해서 좋네요."
  ],
  shipping: "3,000원",
  origin: "일본"
  },
  {
  id: 9, // URL의 ?id=3 과 연결됨
  brand: "PING",
  title: "BLUEPRINT T IRON",
  rating: "4.5",
  reviewCount: 35,
  price: 2130000,
  mainImg: "driver9.png",
  detailImg: "detail9.jpg",
  features: [
    "AI 기술 기반 스마트 립 페이스 적용",
    "안정적인 라이각 및 일관된 롤링",
    "공식 대리점 정품"
  ],
  reviews: [
    "직진성이 매우 뛰어납니다.",
    "그립감이 쫀득해서 좋네요."
  ],
  shipping: "3,000원",
  origin: "일본"
  },
  {
  id: 10, // URL의 ?id=3 과 연결됨
  brand: "PING",
  title: "i540 IRON",
  rating: "4.5",
  reviewCount: 35,
  price: 2280000,
  mainImg: "driver10.png",
  detailImg: "detail10.jpg",
  features: [
    "AI 기술 기반 스마트 립 페이스 적용",
    "안정적인 라이각 및 일관된 롤링",
    "공식 대리점 정품"
  ],
  reviews: [
    "직진성이 매우 뛰어납니다.",
    "그립감이 쫀득해서 좋네요."
  ],
  shipping: "3,000원",
  origin: "일본"
  },
  {
  id: 11, // URL의 ?id=3 과 연결됨
  brand: "Callaway",
  title: "가을 남성 시그니처 로고 티셔츠",
  rating: "4.5",
  reviewCount: 35,
  price: 138000,
  mainImg: "driver11.png",
  detailImg: "detail11.jpg",
  features: [
    "AI 기술 기반 스마트 립 페이스 적용",
    "안정적인 라이각 및 일관된 롤링",
    "공식 대리점 정품"
  ],
  reviews: [
    "직진성이 매우 뛰어납니다.",
    "그립감이 쫀득해서 좋네요."
  ],
  shipping: "3,000원",
  origin: "일본"
  },
  {
  id: 12, // URL의 ?id=3 과 연결됨
  brand: "Callaway",
  title: "여름 여성 홑겹 블루종",
  rating: "4.5",
  reviewCount: 35,
  price: 398000,
  mainImg: "driver12.png",
  detailImg: "detail12.jpg",
  features: [
    "AI 기술 기반 스마트 립 페이스 적용",
    "안정적인 라이각 및 일관된 롤링",
    "공식 대리점 정품"
  ],
  reviews: [
    "직진성이 매우 뛰어납니다.",
    "그립감이 쫀득해서 좋네요."
  ],
  shipping: "3,000원",
  origin: "일본"
  },
  {
  id: 13, // URL의 ?id=3 과 연결됨
  brand: "Callaway",
  title: "[온라인 단독] 크롬투어 트루비스 핫도그 에디션 (공식몰 리미티드)",
  rating: "★★★★★ 5.0",
  reviewCount: 204,
  price: 75900,
  mainImg: "driver13.png",
  detailImgs: [
    "detail13.jpg",
    "detail13-2.jpg"
  ],
  features: [
    "정밀하게 설계된 투어 우레탄 커버",
    "온라인 단독"
  ],
  reviews: [
    "디자인이 댕귀야움.",
    "잘 산거 같아여"
  ],
  shipping: "우체국 택배 / 30만원 이상 결제시 무료배송",
  origin: "Made in USA"
  },
  {
  id: 14, // URL의 ?id=3 과 연결됨
  brand: "Callaway",
  title: "[온라인 단독] 오퍼스 플래티넘 크래프츠맨 컬렉션 웨지: 해머드 카퍼 (공식몰 리미티드)",
  rating: "4.5",
  reviewCount: 35,
  price: 352000,
  mainImg: "driver14.png",
  detailImg: "detail14.jpg",
  features: [
    "AI 기술 기반 스마트 립 페이스 적용",
    "안정적인 라이각 및 일관된 롤링",
    "공식 대리점 정품"
  ],
  reviews: [
    "직진성이 매우 뛰어납니다.",
    "그립감이 쫀득해서 좋네요."
  ],
  shipping: "3,000원",
  origin: "일본"
  },
  {
  id: 15, // URL의 ?id=3 과 연결됨
  brand: "Callaway",
  title: "C-SPROT 스탠드백",
  rating: "4.5",
  reviewCount: 35,
  price: 350000,
  mainImg: "driver15.png",
  detailImg: "detail15.jpg",
  features: [
    "AI 기술 기반 스마트 립 페이스 적용",
    "안정적인 라이각 및 일관된 롤링",
    "공식 대리점 정품"
  ],
  reviews: [
    "직진성이 매우 뛰어납니다.",
    "그립감이 쫀득해서 좋네요."
  ],
  shipping: "3,000원",
  origin: "일본"
  },
  {
  id: 16, // URL의 ?id=3 과 연결됨
  brand: "TAYLORMADE",
  title: "2026 ★특가★ TP5 하프더즌 골프공",
  rating: "4.5",
  reviewCount: 35,
  price: 46000,
  mainImg: "driver16.png",
  detailImg: "detail16.jpg",
  features: [
    "AI 기술 기반 스마트 립 페이스 적용",
    "안정적인 라이각 및 일관된 롤링",
    "공식 대리점 정품"
  ],
  reviews: [
    "직진성이 매우 뛰어납니다.",
    "그립감이 쫀득해서 좋네요."
  ],
  shipping: "3,000원",
  origin: "일본"
  },
  {
  id: 17, // URL의 ?id=3 과 연결됨
  brand: "TAYLORMADE",
  title: "26SS 남성 스트레치 버킷햇 T8031H61628-509",
  rating: "4.5",
  reviewCount: 35,
  price: 118000,
  mainImg: "driver17.png",
  detailImg: "detail17.jpg",
  features: [
    "AI 기술 기반 스마트 립 페이스 적용",
    "안정적인 라이각 및 일관된 롤링",
    "공식 대리점 정품"
  ],
  reviews: [
    "직진성이 매우 뛰어납니다.",
    "그립감이 쫀득해서 좋네요."
  ],
  shipping: "3,000원",
  origin: "일본"
  },
  {
  id: 18, // URL의 ?id=3 과 연결됨
  brand: "TAYLORMADE",
  title: "K-컬렉션 골프 카트백 캐디백 TL885",
  rating: "4.5",
  reviewCount: 35,
  price: 490000,
  mainImg: "driver18.png",
  detailImg: "detail18.jpg",
  features: [
    "AI 기술 기반 스마트 립 페이스 적용",
    "안정적인 라이각 및 일관된 롤링",
    "공식 대리점 정품"
  ],
  reviews: [
    "직진성이 매우 뛰어납니다.",
    "그립감이 쫀득해서 좋네요."
  ],
  shipping: "3,000원",
  origin: "일본"
  },
  {
  id: 19, // URL의 ?id=3 과 연결됨
  brand: "TAYLORMADE",
  title: "26SS 여성 리본 잔플리츠 큐롯 T8031C66491-100",
  rating: "4.5",
  reviewCount: 35,
  price: 258000,
  mainImg: "driver19.png",
  detailImg: "detail19.jpg",
  features: [
    "AI 기술 기반 스마트 립 페이스 적용",
    "안정적인 라이각 및 일관된 롤링",
    "공식 대리점 정품"
  ],
  reviews: [
    "직진성이 매우 뛰어납니다.",
    "그립감이 쫀득해서 좋네요."
  ],
  shipping: "3,000원",
  origin: "일본"
  },
  ] 