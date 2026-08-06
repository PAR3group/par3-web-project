import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, request, redirect, url_for, render_template
from par3.views.auth_views import login_required, admin_required
from par3.models import ShopProduct, ProductReview 
from par3 import db

bp = Blueprint('shop', __name__, url_prefix='/shop')


@bp.route('/')
def main():
    products = ShopProduct.query.all()
    return render_template('shop/shop.html', products=products)


@bp.route('/<int:id>')
def detail(id):
    # [수정] get_or_404로 없는 상품 접근 시 자동으로 404 페이지 처리
    # (기존 JS의 "잘못된 id일 때 alert" 로직을 서버 단에서 처리하는 방식으로 대체)
    product = ShopProduct.query.get_or_404(id)
    return render_template('shop/shop_detail.html', product=product)

# [추가] 상품 등록 "폼 화면"을 보여주는 라우트 (GET) - add_product는 폼 제출 처리(POST)용
@bp.route('/add', methods=['GET'])
@admin_required
def add_product_form():
    return render_template('shop/shop_add.html')

@bp.route('/add', methods=['POST'])
@admin_required                # 관리자만 상품등록 가능
def add_product():
    brand = request.form.get('brand')
    title = request.form.get('title')
    price = request.form.get('price')

    file = request.files.get('main_img')

    if file and file.filename:
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1] if '.' in filename else 'png'
        filename = f"{uuid.uuid4().hex}.{ext}"
        save_path = os.path.join('static', 'img', 'shop_imgs', filename)
        file.save(save_path)
    else:
        filename = 'no_image.png'

    new_product = ShopProduct(
        brand=brand,
        title=title,
        price=int(price),
        main_img=filename,
    )
    db.session.add(new_product)
    db.session.commit()

    return redirect(url_for('shop.main'))


# [추가] 장바구니 담기 API - JS의 fetch('/cart/add')와 연결됨
@bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    # TODO: 실제 장바구니 테이블(Cart 모델) 만들어서 session/user 기준으로 저장하는 로직 필요
    # 지금은 구조만 잡아둔 상태

    return {'success': True, 'product_id': product_id, 'quantity': quantity}