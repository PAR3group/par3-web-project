// [수정] data.js에서 product 찾던 로직 전부 제거 -> HTML에서 이미 <script> 태그로 productId, basePrice를 넘겨받음
document.addEventListener('DOMContentLoaded', () => {
  const quantityInput = document.getElementById('quantity');
  const totalPriceEl = document.getElementById('totalPrice');
  const btnMinus = document.getElementById('btnMinus');
  const btnPlus = document.getElementById('btnPlus');

  let count = 1;

  // 화면에 총 가격 반영하는 함수
  function updatePrice() {
    quantityInput.value = count;
    const total = basePrice * count;
    totalPriceEl.innerText = total.toLocaleString() + '원';
  }

  updatePrice(); // 초기 가격 설정

  btnPlus.addEventListener('click', () => {
    count++;
    updatePrice();
  });

  btnMinus.addEventListener('click', () => {
    if (count > 1) {
      count--;
      updatePrice();
    }
  });

  // [추가] 장바구니/구매 버튼 클릭 시 서버로 요청 보내는 부분 예시 (실제 API 경로에 맞게 수정 필요)
  document.querySelector('.cart').addEventListener('click', () => {
    fetch('/cart/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: productId, quantity: count })
    })
      .then(res => res.json())
      .then(data => alert('장바구니에 담았습니다.'))
      .catch(err => console.error(err));
  });

  document.querySelector('.buy').addEventListener('click', () => {
    location.href = `/order?product_id=${productId}&quantity=${count}`;
  });
});