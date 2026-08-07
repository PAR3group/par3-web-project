// 1. URL에서 상품 ID(?id=1 등) 가져오기
const urlParams = new URLSearchParams(window.location.search);
// URL에 id가 없으면 기본값으로 1번 상품 지정
const productId = parseInt(urlParams.get('id'), 10) || 1;

// 2. data.js의 products 배열에서 해당 상품 데이터 찾기
const product = products.find(p => p.id === productId);

// 만약 존재하지 않는 id인 경우 예외 처리
if (!product) {
  alert("존재하지 않는 상품입니다.");
  window.location.href = "index.html"; // 메인 페이지로 이동
} else {

  // 3. 화면 요소(DOM)에 상품별 데이터 바인딩
 
  // 이미지 & 기본 정보
  document.getElementById('productImg').src = product.mainImg;
  document.getElementById('productImg').alt = product.title;
  document.getElementById('productBrand').textContent = product.brand;
  document.getElementById('productTitle').textContent = product.title;
  document.getElementById('productRating').textContent = product.rating;
  document.getElementById('productReviewCount').textContent = `(${product.reviewCount})`;
 
  // 가격 설정 (data-price 속성 동적 변경)
  const totalPriceElement = document.getElementById('totalPrice');
  totalPriceElement.dataset.price = product.price;

  // 상품 특징 목록 (<ul> 안에 <li> 생성)
  const featuresList = document.getElementById('productFeatures');
  featuresList.innerHTML = ''; // 초기화
  product.features.forEach(text => {
    const li = document.createElement('li');
    li.textContent = text;
    featuresList.appendChild(li);
  });

  // 상품 후기 목록 생성
  const reviewContainer = document.getElementById('reviewContainer');
  reviewContainer.innerHTML = ''; // 초기화
  product.reviews.forEach(reviewText => {
    const reviewBox = document.createElement('div');
    reviewBox.className = 'review-box';
    reviewBox.innerHTML = `
      <span class="review-stars">★★★★★</span>
      <div>${reviewText}</div>
    `;
    reviewContainer.appendChild(reviewBox);
  });

  // 상세 이미지 & 하단 정보 표
  document.getElementById('detailImg').src = product.detailImg;
  document.getElementById('shippingInfo').textContent = product.shipping;
  document.getElementById('originInfo').textContent = product.origin;
}

// 4. 수량 및 동적 가격 계산 로직 (기존 코드 연동)

const quantityInput = document.getElementById('quantity');
const totalPriceElement = document.getElementById('totalPrice');
const btnMinus = document.getElementById('btnMinus');
const btnPlus = document.getElementById('btnPlus');

// 수량 및 가격 업데이트 함수
function updatePrice(quantity) {
  // 화면에 세팅된 data-price 값을 실시간으로 읽어와 단가로 사용
  const unitPrice = parseInt(totalPriceElement.dataset.price, 10);
  const total = unitPrice * quantity;
  totalPriceElement.textContent = total.toLocaleString('ko-KR') + '원';
}

// 최초 1회 가격 표시 업데이트 (1개 가격 계산)
updatePrice(1);

// + 버튼 클릭 이벤트
btnPlus.addEventListener('click', () => {
  let currentQty = parseInt(quantityInput.value, 10);
  currentQty += 1;
  quantityInput.value = currentQty;
  updatePrice(currentQty);
});

// - 버튼 클릭 이벤트
btnMinus.addEventListener('click', () => {
  let currentQty = parseInt(quantityInput.value, 10);
  if (currentQty > 1) {
    currentQty -= 1;
    quantityInput.value = currentQty;
    updatePrice(currentQty);
  }
});